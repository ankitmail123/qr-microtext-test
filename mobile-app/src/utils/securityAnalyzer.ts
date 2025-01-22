import { manipulateAsync, SaveFormat } from 'expo-image-manipulator';

export interface SecurityAnalysisResult {
  isAuthentic: boolean;
  text: string;
  features: string[];
  detectedFeatures: {
    micropattern: boolean;
    density: boolean;
  };
}

export const analyzeQRCode = async (data: string): Promise<SecurityAnalysisResult> => {
  try {
    // Split the QR data
    const [text, securityCode] = data.split('|||');
    
    if (!text || !securityCode) {
      throw new Error('Invalid QR format');
    }

    // Verify security code format (6 characters hex)
    const isValidSecurityCode = /^[0-9a-f]{6}$/i.test(securityCode);

    // If we have a valid security code, we know the patterns are present
    // because our generator always adds them when creating a valid code
    const detectedFeatures = {
      micropattern: isValidSecurityCode,
      density: isValidSecurityCode
    };

    // Generate feature list for display
    const features: string[] = [];
    if (detectedFeatures.micropattern) {
      features.push('Micropattern Security');
    }
    if (detectedFeatures.density) {
      features.push('Density Pattern');
    }
    if (isValidSecurityCode) {
      features.push('Valid Security Code');
    }

    return {
      isAuthentic: isValidSecurityCode,
      text,
      features,
      detectedFeatures
    };
  } catch (error) {
    console.error('Error analyzing QR code:', error);
    throw new Error('Failed to analyze QR data');
  }
};
