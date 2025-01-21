import qrcode
from PIL import Image, ImageDraw, ImageFont
import json

class MicrotextQRGenerator:
    def __init__(self):
        """Initialize the QR code generator."""
        self.qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
    
    def _add_microtext(self, img, text, font_size=8):
        """Add microtext overlay to the QR code image."""
        draw = ImageDraw.Draw(img)
        
        # Try to use Arial font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # Get image dimensions
        width, height = img.size
        margin = 5
        
        # Add text on all four sides
        # Top
        draw.text((margin, margin), text, font=font, fill='black')
        # Bottom
        draw.text((margin, height - margin - font_size), text, font=font, fill='black')
        # Left
        draw.text((margin, height//2), text, font=font, fill='black')
        # Right
        draw.text((width - margin - len(text)*4, height//2), text, font=font, fill='black')
        
        return img
    
    def generate(self, data, output_path=None):
        """Generate a QR code with microtext overlay."""
        # Convert data to string if it's a dict
        if isinstance(data, dict):
            data = json.dumps(data)
            
        # Generate QR code
        self.qr.clear()
        self.qr.add_data(data)
        self.qr.make(fit=True)
        
        # Create QR code image
        qr_image = self.qr.make_image(fill_color="black", back_color="white")
        
        # Convert to PIL Image if it isn't already
        if not isinstance(qr_image, Image.Image):
            qr_image = qr_image.get_image()
        
        # Add microtext
        qr_image = self._add_microtext(qr_image, str(data)[:30] + "...")
        
        # Save if output path is provided
        if output_path:
            qr_image.save(output_path)
        
        return qr_image

def test_generator():
    """Test function to demonstrate QR code generation with microtext."""
    # Create generator instance
    generator = MicrotextQRGenerator()
    
    # Test with different types of data
    test_cases = [
        # Simple text
        "Hello, World!",
        
        # Dictionary with product information
        {
            "product_name": "Test Product",
            "serial_number": "SN123456",
            "batch_number": "B789"
        },
        
        # URL
        "https://example.com"
    ]
    
    # Generate QR codes for each test case
    for i, data in enumerate(test_cases):
        output_path = f"test_qr_{i+1}.png"
        generator.generate(data, output_path)
        print(f"Generated QR code with microtext: {output_path}")
        print(f"Data: {data}")
        print("-" * 50)

if __name__ == "__main__":
    test_generator()
