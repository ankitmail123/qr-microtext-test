# QR Code Generator with Microtext Overlay

A simple Python script to generate QR codes with microtext overlay around the borders.

## Features
- Generate QR codes from text or JSON data
- Add microtext overlay around the QR code borders
- Customizable font size for microtext
- High error correction level for better readability

## Requirements
- Python 3.x
- qrcode
- Pillow (PIL)

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
Run the test script:
```bash
python qr_generator.py
```

This will generate three test QR codes:
1. Simple text QR code
2. QR code with product information
3. QR code with a URL

The generated QR codes will be saved as PNG files in the current directory.

## Customizing the Generator
You can use the `MicrotextQRGenerator` class in your own code:

```python
from qr_generator import MicrotextQRGenerator

# Create generator instance
generator = MicrotextQRGenerator()

# Generate QR code with custom data
data = {
    "product_name": "My Product",
    "serial_number": "123ABC"
}
qr_image = generator.generate(data, "output.png")
```

## Notes
- The microtext uses Arial font by default, falling back to the system default font if Arial is not available
- The QR code uses the highest error correction level (H) to ensure readability even with the microtext overlay
- The microtext is truncated if too long to fit around the borders
