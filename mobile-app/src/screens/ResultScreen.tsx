import React from 'react';
import { StyleSheet, Text, View, ScrollView } from 'react-native';
import { useRoute } from '@react-navigation/native';

export default function ResultScreen() {
  const route = useRoute();
  const params = route.params as {
    text: string;
    isAuthentic: boolean;
    features: string[];
    detectedFeatures: {
      micropattern: boolean;
      density: boolean;
    };
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.title}>Authentication Result</Text>
        <View style={[
          styles.resultBox,
          params.isAuthentic ? styles.authenticBox : styles.invalidBox
        ]}>
          <Text style={styles.resultText}>
            {params.isAuthentic ? 'Authentic QR Code' : 'Invalid QR Code'}
          </Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.title}>Content</Text>
        <Text style={styles.content}>{params.text}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.title}>Security Features</Text>
        <View style={styles.featureList}>
          <View style={styles.featureItem}>
            <Text style={styles.featureLabel}>Micropattern Detection:</Text>
            <Text style={[
              styles.featureStatus,
              params.detectedFeatures?.micropattern ? styles.detected : styles.notDetected
            ]}>
              {params.detectedFeatures?.micropattern ? 'Detected' : 'Not Found'}
            </Text>
          </View>
          
          <View style={styles.featureItem}>
            <Text style={styles.featureLabel}>Density Pattern:</Text>
            <Text style={[
              styles.featureStatus,
              params.detectedFeatures?.density ? styles.detected : styles.notDetected
            ]}>
              {params.detectedFeatures?.density ? 'Detected' : 'Not Found'}
            </Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  section: {
    backgroundColor: '#fff',
    margin: 10,
    padding: 15,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  resultBox: {
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  authenticBox: {
    backgroundColor: '#e8f5e9',
  },
  invalidBox: {
    backgroundColor: '#ffebee',
  },
  resultText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  content: {
    fontSize: 16,
    color: '#333',
  },
  featureList: {
    gap: 10,
  },
  featureItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 10,
    backgroundColor: '#f8f9fa',
    borderRadius: 6,
  },
  featureLabel: {
    fontSize: 14,
    color: '#333',
  },
  featureStatus: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  detected: {
    color: '#4caf50',
  },
  notDetected: {
    color: '#f44336',
  },
});
