import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StyleSheet, View, Text } from 'react-native';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import ScannerScreen from './src/screens/ScannerScreen';
import ResultScreen from './src/screens/ResultScreen';

export const APP_VERSION = "1.1.3";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen 
            name="Home" 
            component={HomeScreen}
            options={{title: 'Secure QR Scanner'}}
          />
          <Stack.Screen 
            name="Scanner" 
            component={ScannerScreen}
            options={{ 
              title: `Secure QR Scanner v${APP_VERSION}`,
              headerStyle: {
                backgroundColor: '#2196F3',
              },
              headerTintColor: '#fff',
            }}
          />
          <Stack.Screen 
            name="Result" 
            component={ResultScreen}
            options={{ 
              title: 'Scan Result',
              headerStyle: {
                backgroundColor: '#2196F3',
              },
              headerTintColor: '#fff',
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
