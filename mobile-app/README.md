# Secure QR Scanner Mobile App

A React Native mobile application for scanning and verifying secure QR codes with advanced security features.

## Features

- Scan QR codes with camera integration
- Detect security features:
  - Micropattern detection
  - Density variation analysis
- Real-time authenticity verification
- Dark mode support
- Modern, user-friendly interface

## Requirements

- Node.js 14+
- npm or yarn
- Expo CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ankitmail123/SecureQRScanner.git
cd SecureQRScanner
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npx expo start
```

4. Run on your device:
   - Install Expo Go on your mobile device
   - Scan the QR code shown in the terminal
   - The app will load on your device

## Security Features

The app verifies two types of security features in QR codes:

1. **Micropattern Detection**
   - Analyzes high-contrast microscopic patterns
   - Verifies pattern authenticity
   - Resistant to photocopying

2. **Density Pattern Analysis**
   - Checks for specific density variations
   - Validates pattern consistency
   - Detects unauthorized duplicates

## QR Code Format

The app expects QR codes in the following format:
```
text|||securityCode
```
where:
- `text`: The actual content to display
- `securityCode`: Base64-encoded JSON containing security patterns

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Version History

- v1.1: Added security feature detection and verification
- v1.0: Initial release with basic QR scanning
