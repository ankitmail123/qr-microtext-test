import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Dimensions } from 'react-native';
import { Camera, CameraType } from 'expo-camera';
import { BarCodeScanner } from 'expo-barcode-scanner';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { analyzeQRSecurity } from '../utils/securityAnalyzer';

const SCREEN_WIDTH = Dimensions.get('window').width;
const SCREEN_HEIGHT = Dimensions.get('window').height;
const SCAN_AREA_SIZE = SCREEN_WIDTH * 0.7;

type RootStackParamList = {
  Scanner: undefined;
  Result: {
    isAuthentic: boolean;
    text: string;
    features: {
      micropattern: boolean;
      densityVariation: boolean;
    };
  };
};

type ScannerScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Scanner'>;
};

export default function ScannerScreen({ navigation }: ScannerScreenProps) {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [scanned, setScanned] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const cameraRef = useRef<Camera>(null);

  useEffect(() => {
    const getBarCodeScannerPermissions = async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    };

    getBarCodeScannerPermissions();
  }, []);

  const handleBarCodeScanned = async ({ type, data, bounds }: { type: string; data: string; bounds: any }) => {
    if (scanned || isAnalyzing) return;
    
    try {
      setIsAnalyzing(true);
      setScanned(true);

      // Capture the frame
      if (!cameraRef.current) return;
      
      const photo = await cameraRef.current.takePictureAsync({
        quality: 1,
        base64: true,
        skipProcessing: true
      });

      // Analyze security features
      const analysisResult = await analyzeQRSecurity(data, photo.uri);

      // Navigate to results
      navigation.navigate('Result', {
        isAuthentic: analysisResult.isAuthentic,
        text: analysisResult.text,
        features: {
          micropattern: analysisResult.detectedFeatures.micropattern,
          densityVariation: analysisResult.detectedFeatures.density
        }
      });
    } catch (error) {
      console.error('Error processing QR code:', error);
      alert('Failed to analyze QR code. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  if (hasPermission === null) {
    return <View style={styles.container}><Text>Requesting camera permission...</Text></View>;
  }
  if (hasPermission === false) {
    return <View style={styles.container}><Text>No access to camera</Text></View>;
  }

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFillObject}
        type={CameraType.back}
        barCodeScannerSettings={{
          barCodeTypes: [BarCodeScanner.Constants.BarCodeType.qr],
        }}
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
      >
        <View style={styles.overlay}>
          <View style={styles.scanArea} />
        </View>
        
        <View style={styles.bottomBar}>
          <Text style={styles.instructions}>
            {isAnalyzing ? 'Analyzing security features...' : 'Position the QR code within the frame'}
          </Text>
          {scanned && !isAnalyzing && (
            <TouchableOpacity
              style={styles.scanButton}
              onPress={() => setScanned(false)}>
              <Text style={styles.scanButtonText}>Tap to Scan Again</Text>
            </TouchableOpacity>
          )}
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  scanArea: {
    width: SCAN_AREA_SIZE,
    height: SCAN_AREA_SIZE,
    borderWidth: 2,
    borderColor: '#FFF',
    backgroundColor: 'transparent',
  },
  bottomBar: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: 20,
    backgroundColor: 'rgba(0,0,0,0.8)',
    alignItems: 'center',
  },
  instructions: {
    color: '#FFF',
    textAlign: 'center',
    fontSize: 16,
    marginBottom: 10,
  },
  scanButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 25,
    marginTop: 10,
  },
  scanButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '600',
  },
});
