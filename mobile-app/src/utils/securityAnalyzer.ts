import { manipulateAsync, SaveFormat } from 'expo-image-manipulator';
import * as FileSystem from 'expo-file-system';
import { decode as base64Decode } from 'base-64';

export interface SecurityAnalysisResult {
  isAuthentic: boolean;
  text: string;
  features: string[];
  detectedFeatures: {
    micropattern: boolean;
    density: boolean;
  };
  hasValidSecurityCode?: boolean;
  hasSecurityFeatures?: boolean;
}

async function detectMicropattern(imageData: string, securityCode: string): Promise<boolean> {
  try {
    // Decode base64 directly
    const binaryString = base64Decode(imageData);
    const pixels = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      pixels[i] = binaryString.charCodeAt(i);
    }
    
    // Parse security code for pattern parameters
    const hexValues = [];
    for (let i = 0; i < 6; i += 2) {
      hexValues.push(parseInt(securityCode.slice(i, i + 2), 16));
    }
    
    // Extract expected pattern parameters
    const patternSize = 5;  // Fixed size
    const patternSpacing = 20;  // Fixed spacing
    const patternIntensity = 130 + (hexValues[0] % 61);  // 130-190 range
    const patternRotation = (hexValues[1] % 4) * 45;  // 0, 45, 90, or 135 degrees
    const patternStyle = hexValues[2] % 4;  // 4 different styles
    
    // Define pattern templates
    const patterns = [
      [[0,0], [0,4], [1,1], [1,3], [2,0], [2,2], [2,4], [3,1], [3,3], [4,0], [4,4]],  // X pattern
      [[0,2], [1,1], [1,2], [1,3], [2,0], [2,1], [2,2], [2,3], [2,4], [3,1], [3,2], [3,3], [4,2]],  // + pattern
      [[0,0], [0,2], [0,4], [2,0], [2,2], [2,4], [4,0], [4,2], [4,4]],  // 9-dot pattern
      [[0,1], [0,3], [1,0], [1,4], [2,2], [3,0], [3,4], [4,1], [4,3]]  // diamond pattern
    ];
    const selectedPattern = patterns[patternStyle];
    
    // Calculate image dimensions
    const width = Math.sqrt(pixels.length / 4);
    const height = width;
    
    // Helper function to rotate points
    function rotatePoint(x: number, y: number, angle: number): [number, number] {
      const rad = angle * Math.PI / 180;
      const cos = Math.cos(rad);
      const sin = Math.sin(rad);
      return [
        Math.round(x * cos - y * sin),
        Math.round(x * sin + y * cos)
      ];
    }
    
    // Count matching patterns
    let matchingPatterns = 0;
    let totalPatterns = 0;
    
    // Scan for patterns
    for (let baseY = patternSize; baseY < height - patternSize; baseY += patternSpacing) {
      for (let baseX = patternSize; baseX < width - patternSize; baseX += patternSpacing) {
        // Check if this is a white area
        const pos = (baseY * width + baseX) * 4;
        if (pos >= pixels.length - 4) continue;
        
        const r = pixels[pos];
        const g = pixels[pos + 1];
        const b = pixels[pos + 2];
        
        if (r > 240 && g > 240 && b > 240) {
          totalPatterns++;
          
          // Check for pattern match
          let matchingPixels = 0;
          let totalChecks = 0;
          
          for (const [dotX, dotY] of selectedPattern) {
            // Apply rotation
            const [rx, ry] = rotatePoint(
              dotX - patternSize/2,
              dotY - patternSize/2,
              patternRotation
            );
            const px = baseX + rx + Math.floor(patternSize/2);
            const py = baseY + ry + Math.floor(patternSize/2);
            
            if (px >= 0 && px < width && py >= 0 && py < height) {
              const pixelPos = (py * width + px) * 4;
              if (pixelPos >= pixels.length - 4) continue;
              
              const pr = pixels[pixelPos];
              const pg = pixels[pixelPos + 1];
              const pb = pixels[pixelPos + 2];
              
              // Calculate expected intensity with position variation
              const posVar = ((px * py) % 20) - 10;
              const expectedIntensity = patternIntensity + posVar;
              
              // Allow for intensity variation
              const intensityRange = 25;
              if (Math.abs(pr - expectedIntensity) <= intensityRange &&
                  Math.abs(pg - expectedIntensity) <= intensityRange &&
                  Math.abs(pb - expectedIntensity) <= intensityRange) {
                matchingPixels++;
              }
              totalChecks++;
            }
          }
          
          // Consider pattern matching if most pixels match
          if (totalChecks > 0 && matchingPixels / totalChecks >= 0.6) {
            matchingPatterns++;
          }
        }
      }
    }
    
    const matchRatio = matchingPatterns / (totalPatterns || 1);
    console.log('Micropattern analysis:', {
      matchingPatterns,
      totalPatterns,
      matchRatio,
      expectedParams: {
        intensity: patternIntensity,
        rotation: patternRotation,
        style: patternStyle
      }
    });
    
    // We expect to find matching patterns in 15-50% of the expected positions
    return matchRatio >= 0.15 && matchRatio <= 0.5 && totalPatterns > 15;
  } catch (error) {
    console.error('Error detecting micropattern:', error);
    return false;
  }
}

async function detectDensityPattern(imageData: string, securityCode: string): Promise<boolean> {
  try {
    // Decode base64 directly
    const binaryString = base64Decode(imageData);
    const pixels = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      pixels[i] = binaryString.charCodeAt(i);
    }
    
    // Parse security code for pattern parameters
    const hexValues = [];
    for (let i = 0; i < 6; i += 2) {
      hexValues.push(parseInt(securityCode.slice(i, i + 2), 16));
    }
    
    // Extract expected pattern parameters
    const cellSize = 10;  // Fixed size
    const baseIntensity = 220 + (hexValues[0] % 20);  // 220-240 base
    const patternType = hexValues[1] % 4;  // 4 different types
    const intensityRange = 10 + (hexValues[2] % 11);  // 10-20 range
    
    // Calculate image dimensions
    const width = Math.sqrt(pixels.length / 4);
    const height = width;
    
    // Count matching cells
    let matchingCells = 0;
    let totalCells = 0;
    
    for (let y = 0; y < height - cellSize; y += cellSize) {
      for (let x = 0; x < width - cellSize; x += cellSize) {
        // Check if this is a white area
        const pos = (y * width + x) * 4;
        if (pos >= pixels.length - 4) continue;
        
        const r = pixels[pos];
        const g = pixels[pos + 1];
        const b = pixels[pos + 2];
        
        if (r > 240 && g > 240 && b > 240) {
          totalCells++;
          
          // Calculate expected intensity based on pattern type
          let expectedMod = 0;
          if (patternType === 0) {
            // Checkerboard
            expectedMod = ((x/cellSize + y/cellSize) % 2 === 0) ? intensityRange : 0;
          } else if (patternType === 1) {
            // Diagonal stripes
            expectedMod = ((x + y) % (cellSize * 2) < cellSize) ? intensityRange : 0;
          } else if (patternType === 2) {
            // Radial
            const dx = x - width/2;
            const dy = y - height/2;
            const dist = Math.sqrt(dx*dx + dy*dy);
            expectedMod = Math.round((Math.cos(dist/20) + 1) * intensityRange/2);
          } else {
            // Wavy
            expectedMod = Math.round(Math.sin(x/10) * Math.cos(y/10) * intensityRange);
          }
          
          const expectedIntensity = baseIntensity - expectedMod;
          
          // Sample multiple points in the cell
          let matchingPoints = 0;
          let totalPoints = 0;
          
          for (let sy = 0; sy < cellSize; sy += 2) {  // Sample every 2nd pixel
            for (let sx = 0; sx < cellSize; sx += 2) {
              const samplePos = ((y + sy) * width + (x + sx)) * 4;
              if (samplePos >= pixels.length - 4) continue;
              
              const sr = pixels[samplePos];
              const sg = pixels[samplePos + 1];
              const sb = pixels[samplePos + 2];
              
              // Calculate average intensity
              const actualIntensity = (sr + sg + sb) / 3;
              
              // Allow for intensity variation
              if (Math.abs(actualIntensity - expectedIntensity) <= 15) {
                matchingPoints++;
              }
              totalPoints++;
            }
          }
          
          // Consider cell matching if most sampled points match
          if (totalPoints > 0 && matchingPoints / totalPoints >= 0.4) {
            matchingCells++;
          }
        }
      }
    }
    
    const matchRatio = matchingCells / (totalCells || 1);
    console.log('Density pattern analysis:', {
      matchingCells,
      totalCells,
      matchRatio,
      expectedParams: {
        baseIntensity,
        patternType,
        intensityRange
      }
    });
    
    // We expect to find matching cells in 10-50% of white areas
    return matchRatio >= 0.1 && matchRatio <= 0.5 && totalCells > 25;
  } catch (error) {
    console.error('Error detecting density pattern:', error);
    return false;
  }
}

export async function analyzeQRCode(data: string, imageData: string): Promise<SecurityAnalysisResult> {
  try {
    // Split the QR data to get text and security code
    const [text, securityCode] = data.split('|||');
    console.log('Analyzing QR:', { text, securityCode });

    // Check for security features in the image
    const [micropatternDetected, densityDetected] = await Promise.all([
      detectMicropattern(imageData, securityCode),
      detectDensityPattern(imageData, securityCode)
    ]);

    console.log('Security Feature Detection:', {
      micropatternDetected,
      densityDetected
    });

    // A QR is authentic only if it has BOTH:
    // 1. A valid security code in the QR data
    // 2. Detectable security features in the image
    const hasValidSecurityCode = !!securityCode && securityCode.length === 6;
    const hasSecurityFeatures = micropatternDetected && densityDetected; // Need BOTH features

    return {
      text: text || data,
      isAuthentic: hasValidSecurityCode && hasSecurityFeatures,
      features: ['micropattern', 'density'],
      detectedFeatures: {
        micropattern: micropatternDetected,
        density: densityDetected
      },
      hasValidSecurityCode,
      hasSecurityFeatures
    };
  } catch (error) {
    console.error('Error analyzing QR code:', error);
    return {
      text: data,
      isAuthentic: false,
      features: [],
      detectedFeatures: {
        micropattern: false,
        density: false
      }
    };
  }
}
