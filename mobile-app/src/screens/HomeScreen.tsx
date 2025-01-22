import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  useColorScheme,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Scanner: undefined;
  Result: undefined;
};

type HomeScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Home'>;
};

const HomeScreen = ({ navigation }: HomeScreenProps) => {
  const isDarkMode = useColorScheme() === 'dark';

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={[styles.title, isDarkMode && styles.darkText]}>
          Secure QR Scanner
        </Text>
        <Text style={[styles.subtitle, isDarkMode && styles.darkText]}>
          Verify authenticity of secure QR codes
        </Text>
        
        <View style={styles.featuresContainer}>
          <Text style={[styles.featuresTitle, isDarkMode && styles.darkText]}>
            Features:
          </Text>
          <Text style={[styles.featureItem, isDarkMode && styles.darkText]}>
            • Detect micropattern security features
          </Text>
          <Text style={[styles.featureItem, isDarkMode && styles.darkText]}>
            • Identify density variations
          </Text>
          <Text style={[styles.featureItem, isDarkMode && styles.darkText]}>
            • Distinguish original from copies
          </Text>
        </View>

        <TouchableOpacity
          style={styles.scanButton}
          onPress={() => navigation.navigate('Scanner')}>
          <Text style={styles.scanButtonText}>Start Scanning</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#000',
    marginTop: 20,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
  },
  featuresContainer: {
    width: '100%',
    padding: 20,
    backgroundColor: '#f5f5f5',
    borderRadius: 10,
    marginBottom: 30,
  },
  featuresTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#000',
  },
  featureItem: {
    fontSize: 16,
    color: '#333',
    marginBottom: 8,
    paddingLeft: 10,
  },
  scanButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 25,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  scanButtonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: '600',
  },
  darkText: {
    color: '#FFFFFF',
  },
});

export default HomeScreen;
