# Secure QR Code Generator

A Python script to generate secure QR codes with machine-detectable anti-copying features.

## Features
- Generate QR codes with two types of security features:
  1. **Micropattern QR**: High-contrast microscopic dot patterns optimized for mobile scanning
  2. **Density Variation QR**: Binary density patterns that become uniform when copied
- Security patterns are deterministically generated from a security code
- Optimized for small-scale printing (20mm x 20mm)
- Machine-detectable security features
- High error correction level for better readability

## Requirements
- Python 3.x
- qrcode
- Pillow (PIL)
- numpy
- matplotlib (for visualization)

## Installation
1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Generate secure QR codes with custom text and security code:
```bash
python qr_generator.py "your_text" "your_security_code"
```

Example:
```bash
python qr_generator.py "Hello World" "SEC123"
```

This will generate two QR codes:
1. `secure_qr_micropattern_mini.png`: QR code with microscopic dot patterns
2. `secure_qr_density_variation_mini.png`: QR code with density variation patterns

## Printing Instructions
For optimal results:
1. Minimum printer resolution: 300 DPI
2. Use high-quality paper (at least 80 gsm)
3. Ensure printer is calibrated for sharp black output
4. No scaling during printing (print at 100% size)
5. Verify printed size is exactly 20mm x 20mm

## Security Features
1. **Micropattern QR**
   - High-contrast microscopic dot patterns
   - Patterns are derived from security code
   - Optimized for mobile scanning
   - Breaks when photocopied

2. **Density Variation QR**
   - Binary density patterns
   - Pattern angles influenced by security code
   - Becomes uniform when copied
   - Machine-detectable variations

## Notes
- Security patterns are designed for machine detection, not visual verification
- QR codes use high error correction level (H) for reliability
- Patterns are deterministically generated from the security code
- Output size is optimized for 20mm x 20mm printing
