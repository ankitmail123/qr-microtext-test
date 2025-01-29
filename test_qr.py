import qrcode
from PIL import Image, ImageDraw
import hashlib
import math
import numpy as np

def add_security_features(image, features, security_code):
    # Convert to RGBA for transparency support
    image = image.convert('RGBA')
    width, height = image.size
    pixels = image.load()
    draw = ImageDraw.Draw(image)
    
    # Convert security code to pattern parameters
    hex_values = [int(security_code[i:i+2], 16) for i in range(0, 6, 2)]
    
    # Create a unique cross pattern based on security code
    pattern_size = 5  # Fixed size for better detection
    pattern_spacing = 20  # Fixed spacing for better detection
    
    # Use security code to determine pattern variations
    pattern_intensity = 130 + (hex_values[0] % 61)  # 130-190 range
    pattern_rotation = (hex_values[1] % 4) * 45  # 0, 45, 90, or 135 degrees
    pattern_style = hex_values[2] % 4  # 4 different pattern styles
    
    # Pattern styles (cross variations)
    patterns = [
        [(0,0), (0,4), (1,1), (1,3), (2,0), (2,2), (2,4), (3,1), (3,3), (4,0), (4,4)],  # X pattern
        [(0,2), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3), (2,4), (3,1), (3,2), (3,3), (4,2)],  # + pattern
        [(0,0), (0,2), (0,4), (2,0), (2,2), (2,4), (4,0), (4,2), (4,4)],  # 9-dot pattern
        [(0,1), (0,3), (1,0), (1,4), (2,2), (3,0), (3,4), (4,1), (4,3)]  # diamond pattern
    ]
    selected_pattern = patterns[pattern_style]
    
    def rotate_point(x, y, angle):
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return (int(x * cos_a - y * sin_a), int(x * sin_a + y * cos_a))
    
    # Add patterns in white areas
    for base_y in range(pattern_size, height - pattern_size, pattern_spacing):
        for base_x in range(pattern_size, width - pattern_size, pattern_spacing):
            # Check if area is white and away from QR code
            is_white_area = True
            has_qr_nearby = False
            
            for check_y in range(-2, pattern_size + 3):
                for check_x in range(-2, pattern_size + 3):
                    px = base_x + check_x
                    py = base_y + check_y
                    if 0 <= px < width and 0 <= py < height:
                        r, g, b, a = pixels[px, py]
                        if r < 200:  # If pixel is not white-ish
                            is_white_area = False
                            break
                if not is_white_area:
                    break
            
            if is_white_area:
                # Add rotated pattern
                for point in selected_pattern:
                    x, y = rotate_point(point[0] - pattern_size//2, point[1] - pattern_size//2, pattern_rotation)
                    px = base_x + x + pattern_size//2
                    py = base_y + y + pattern_size//2
                    if 0 <= px < width and 0 <= py < height:
                        pixels[px, py] = (pattern_intensity, pattern_intensity, pattern_intensity, 255)
    
    # Add density pattern
    density_pattern_size = 2
    for y in range(0, height, density_pattern_size):
        for x in range(0, width, density_pattern_size):
            # Check if area is white
            is_white = True
            for cy in range(density_pattern_size):
                for cx in range(density_pattern_size):
                    px = x + cx
                    py = y + cy
                    if px < width and py < height:
                        r, g, b, a = pixels[px, py]
                        if r < 200:
                            is_white = False
                            break
                if not is_white:
                    break
            
            if is_white:
                # Create checkerboard pattern with intensity variation
                intensity_base = 220 + (hex_values[0] % 21)  # 220-240 range
                intensity_var = 10
                for cy in range(density_pattern_size):
                    for cx in range(density_pattern_size):
                        if (x + y) % 4 == 0:  # Checkerboard pattern
                            final_intensity = intensity_base + ((cx + cy) % 2) * intensity_var
                        else:
                            final_intensity = intensity_base - ((cx + cy) % 2) * intensity_var
                        px = x + cx
                        py = y + cy
                        if px < width and py < height:
                            pixels[px, py] = (final_intensity, final_intensity, final_intensity, 255)
    
    return image

def create_secure_qr(text, security_code):
    """Create a QR code with security features"""
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Add security features
    img = add_security_features(img, ['micropattern', 'density'], security_code)
    
    return img

def test_qr_codes():
    text = "12345"
    security_codes = [
        "a1b2c3",  # Will create X pattern with 90° rotation
        "d4e5f6",  # Will create + pattern with 45° rotation
        "789abc"   # Will create 9-dot pattern with 135° rotation
    ]
    
    # Generate QR codes with different security patterns
    for i, security_code in enumerate(security_codes, 1):
        # Create secure QR
        qr = create_secure_qr(text, security_code)
        qr.save(f"test_secure_{i}.png")
        
        print(f"\nTest Case {i}:")
        print(f"Text: {text}")
        print(f"Security Code: {security_code}")
        print(f"Generated secure QR: test_secure_{i}.png")
        
        # Print expected pattern details
        hex_values = [int(security_code[i:i+2], 16) for i in range(0, 6, 2)]
        pattern_intensity = 130 + (hex_values[0] % 61)
        pattern_rotation = (hex_values[1] % 4) * 45
        pattern_style = hex_values[2] % 4
        styles = ["X", "+", "9-dot", "diamond"]
        
        print(f"Expected Pattern:")
        print(f"- Style: {styles[pattern_style]}")
        print(f"- Rotation: {pattern_rotation}°")
        print(f"- Intensity: {pattern_intensity}")

if __name__ == "__main__":
    test_qr_codes()
