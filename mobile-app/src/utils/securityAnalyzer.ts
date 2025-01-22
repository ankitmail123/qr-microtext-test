import { manipulateAsync, SaveFormat } from 'expo-image-manipulator';
import * as ImageManipulator from 'expo-image-manipulator';

interface SecurityPattern {
  type: 'micropattern' | 'density';
  value: string;
}

interface QRContent {
  text: string;
  securityCode: string;
}

export interface SecurityAnalysisResult {
  isAuthentic: boolean;
  text: string;
  detectedFeatures: {
    micropattern: boolean;
    density: boolean;
  };
}

// Parse QR content to separate text and security code
const parseQRContent = (data: string): QRContent => {
  try {
    // Expected format: text|||securityCode
    const [text, securityCode] = data.split('|||');
    if (!text || !securityCode) {
      throw new Error('Invalid QR format');
    }
    return { text, securityCode };
  } catch (error) {
    throw new Error('Invalid QR code format');
  }
};

// Decode security code to get expected patterns
const decodeSecurityCode = (securityCode: string): SecurityPattern[] => {
  try {
    // Security code format: base64(JSON([{type, value}]))
    const decoded = Buffer.from(securityCode, 'base64').toString('utf-8');
    const patterns: SecurityPattern[] = JSON.parse(decoded);
    return patterns;
  } catch (error) {
    throw new Error('Invalid security code');
  }
};

// Analyze image for micropattern
const detectMicropattern = async (imageUri: string, expectedPattern: string): Promise<boolean> => {
  try {
    // Convert image to grayscale and increase contrast for pattern detection
    const processed = await manipulateAsync(
      imageUri,
      [
        { resize: { width: 300 } },
        { contrast: 1.5 },
        { brightness: 1.2 }
      ],
      { format: SaveFormat.PNG }
    );

    // Analyze central region for micropattern
    // This is where we'd implement actual pattern matching
    // For now, we'll check if the pattern string exists in the QR data
    return true; // Replace with actual pattern detection
  } catch (error) {
    console.error('Micropattern detection error:', error);
    return false;
  }
};

// Analyze image for density variations
const detectDensityPattern = async (imageUri: string, expectedPattern: string): Promise<boolean> => {
  try {
    // Convert image to binary for density analysis
    const processed = await manipulateAsync(
      imageUri,
      [
        { resize: { width: 300 } },
        { contrast: 2 }
      ],
      { format: SaveFormat.PNG }
    );

    // Analyze density distribution
    // This is where we'd implement actual density analysis
    // For now, we'll check if the pattern string exists in the QR data
    return true; // Replace with actual density analysis
  } catch (error) {
    console.error('Density pattern detection error:', error);
    return false;
  }
};

export const analyzeQRSecurity = async (
  data: string,
  imageUri: string
): Promise<SecurityAnalysisResult> => {
  try {
    // Parse QR content
    const { text, securityCode } = parseQRContent(data);
    
    // Decode security patterns
    const patterns = decodeSecurityCode(securityCode);
    
    // Initialize results
    const detectedFeatures = {
      micropattern: false,
      density: false
    };

    // Check each security feature
    for (const pattern of patterns) {
      if (pattern.type === 'micropattern') {
        detectedFeatures.micropattern = await detectMicropattern(imageUri, pattern.value);
      } else if (pattern.type === 'density') {
        detectedFeatures.density = await detectDensityPattern(imageUri, pattern.value);
      }
    }

    // Determine authenticity
    const isAuthentic = patterns.every(pattern => 
      (pattern.type === 'micropattern' && detectedFeatures.micropattern) ||
      (pattern.type === 'density' && detectedFeatures.density)
    );

    return {
      isAuthentic,
      text,
      detectedFeatures
    };
  } catch (error) {
    console.error('Security analysis error:', error);
    throw new Error('Failed to analyze QR code security');
  }
};
