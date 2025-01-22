import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, Text, View, Button, Alert, ActivityIndicator } from 'react-native';
import { Camera } from 'expo-camera';
import { analyzeQRCode } from '../utils/securityAnalyzer';
import { useNavigation, useIsFocused } from '@react-navigation/native';

export default function ScannerScreen() {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [scanned, setScanned] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const navigation = useNavigation();
  const isFocused = useIsFocused();
  const cameraRef = useRef<Camera | null>(null);

  useEffect(() => {
    const getBarCodeScannerPermissions = async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    };

    getBarCodeScannerPermissions();
  }, []);

  useEffect(() => {
    if (!isFocused) {
      setScanned(false);
      setIsProcessing(false);
    }
  }, [isFocused]);

  const handleBarCodeScanned = async ({ data }: { type: string; data: string }) => {
    if (scanned || isProcessing || !isFocused) return;
    
    try {
      setIsProcessing(true);
      console.log('Scanned data:', data);

      // Analyze the QR code
      const result = await analyzeQRCode(data);
      console.log('Analysis result:', result);

      // Navigate to result screen with all the data
      navigation.navigate('Result', {
        text: result.text,
        isAuthentic: result.isAuthentic,
        features: result.features,
        detectedFeatures: result.detectedFeatures
      });
    } catch (error) {
      console.error('Scanning error:', error);
      Alert.alert(
        'Invalid QR Code',
        'This QR code lacks required security features. Please scan a valid secure QR code.',
        [{ text: 'Try Again', onPress: () => {
          setScanned(false);
          setIsProcessing(false);
        }}]
      );
    } finally {
      setScanned(true);
      setIsProcessing(false);
    }
  };

  if (hasPermission === null) {
    return <Text style={styles.text}>Requesting camera permission...</Text>;
  }
  if (hasPermission === false) {
    return <Text style={styles.text}>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      {isFocused && (
        <Camera
          ref={cameraRef}
          style={styles.camera}
          type={Camera.Constants.Type.back}
          onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
          ratio="16:9"
        >
          <View style={styles.overlay}>
            <View style={styles.scanArea} />
            {isProcessing ? (
              <View style={styles.processingContainer}>
                <ActivityIndicator size="large" color="#fff" />
                <Text style={styles.scanText}>Processing QR Code...</Text>
              </View>
            ) : (
              <Text style={styles.scanText}>
                Align QR code within the frame
              </Text>
            )}
          </View>
        </Camera>
      )}
      {scanned && !isProcessing && (
        <View style={styles.buttonContainer}>
          <Button 
            title="Scan Another Code" 
            onPress={() => {
              setScanned(false);
              setIsProcessing(false);
            }} 
          />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  scanArea: {
    width: 250,
    height: 250,
    borderWidth: 2,
    borderColor: '#fff',
    backgroundColor: 'transparent',
  },
  buttonContainer: {
    padding: 16,
    backgroundColor: '#fff',
  },
  text: {
    flex: 1,
    fontSize: 16,
    textAlign: 'center',
    padding: 20,
    color: '#fff',
    backgroundColor: '#000',
  },
  scanText: {
    color: '#fff',
    fontSize: 16,
    marginTop: 20,
    textAlign: 'center',
  },
  processingContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
});
