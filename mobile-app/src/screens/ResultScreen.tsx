import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  useColorScheme,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RouteProp } from '@react-navigation/native';

type RootStackParamList = {
  Result: {
    isAuthentic: boolean;
    text: string;
    features: {
      micropattern: boolean;
      densityVariation: boolean;
    };
  };
};

type ResultScreenProps = {
  route: RouteProp<RootStackParamList, 'Result'>;
  navigation: NativeStackNavigationProp<RootStackParamList, 'Result'>;
};

const ResultScreen = ({ route, navigation }: ResultScreenProps) => {
  const { isAuthentic, text, features } = route.params;
  const isDarkMode = useColorScheme() === 'dark';

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View
          style={[
            styles.resultBanner,
            { backgroundColor: isAuthentic ? '#4CAF50' : '#F44336' },
          ]}>
          <Text style={styles.resultText}>
            {isAuthentic ? 'Authentic QR Code' : 'Invalid QR Code'}
          </Text>
        </View>

        <View style={styles.contentContainer}>
          <Text style={[styles.sectionTitle, isDarkMode && styles.darkText]}>
            Content
          </Text>
          <View style={styles.textContainer}>
            <Text style={[styles.contentText, isDarkMode && styles.darkText]}>
              {text}
            </Text>
          </View>
        </View>

        <View style={styles.featuresContainer}>
          <Text style={[styles.sectionTitle, isDarkMode && styles.darkText]}>
            Security Analysis
          </Text>

          <View style={styles.featureItem}>
            <Text style={[styles.featureTitle, isDarkMode && styles.darkText]}>
              Micropattern Detection
            </Text>
            <View
              style={[
                styles.featureStatus,
                {
                  backgroundColor: features.micropattern ? '#E8F5E9' : '#FFEBEE',
                },
              ]}>
              <Text
                style={[
                  styles.featureStatusText,
                  {
                    color: features.micropattern ? '#2E7D32' : '#C62828',
                  },
                ]}>
                {features.micropattern ? 'VERIFIED' : 'NOT FOUND'}
              </Text>
            </View>
          </View>

          <View style={styles.featureItem}>
            <Text style={[styles.featureTitle, isDarkMode && styles.darkText]}>
              Density Pattern
            </Text>
            <View
              style={[
                styles.featureStatus,
                {
                  backgroundColor: features.densityVariation
                    ? '#E8F5E9'
                    : '#FFEBEE',
                },
              ]}>
              <Text
                style={[
                  styles.featureStatusText,
                  {
                    color: features.densityVariation ? '#2E7D32' : '#C62828',
                  },
                ]}>
                {features.densityVariation ? 'VERIFIED' : 'NOT FOUND'}
              </Text>
            </View>
          </View>
        </View>

        <TouchableOpacity
          style={styles.scanButton}
          onPress={() => navigation.navigate('Scanner')}>
          <Text style={styles.scanButtonText}>Scan Another Code</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF',
  },
  scrollContent: {
    padding: 20,
  },
  resultBanner: {
    padding: 15,
    borderRadius: 8,
    marginBottom: 20,
  },
  resultText: {
    color: '#FFF',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  contentContainer: {
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 15,
    marginBottom: 20,
  },
  textContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 4,
    padding: 10,
    marginTop: 10,
  },
  contentText: {
    fontSize: 16,
    color: '#000000',
    lineHeight: 24,
  },
  featuresContainer: {
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 15,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#000',
  },
  featureItem: {
    marginBottom: 20,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#000',
  },
  featureStatus: {
    padding: 8,
    borderRadius: 4,
    marginBottom: 8,
  },
  featureStatusText: {
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  scanButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  scanButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '600',
  },
  darkText: {
    color: '#FFFFFF',
  },
});

export default ResultScreen;
