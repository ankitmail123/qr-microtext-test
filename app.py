from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import os
import secrets
import numpy as np
import hashlib
import math

VERSION = "1.2.1"
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate_pattern_points(security_code, width, height, spacing):
    """Generate pattern points based on security code"""
    # Use security code to seed the pattern
    hash_obj = hashlib.sha256(security_code.encode())
    seed = int(hash_obj.hexdigest()[:8], 16)
    np.random.seed(seed)
    
    points = []
    for x in range(0, width, spacing):
        for y in range(0, height, spacing):
            # Use security code to determine if this point should be included
            if np.random.random() > 0.4:  # 60% chance of including point
                points.append((x, y))
    return points

def add_security_features(image, features, security_code):
    # Convert to RGBA for transparency support
    image = image.convert('RGBA')
    width, height = image.size
    pixels = image.load()
    draw = ImageDraw.Draw(image)
    
    if 'micropattern' in features:
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
            import math
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
                            if r < 240 or g < 240 or b < 240:
                                is_white_area = False
                            if r < 50 and g < 50 and b < 50:
                                has_qr_nearby = True
                                break
                    if not is_white_area or has_qr_nearby:
                        break
                
                if is_white_area and not has_qr_nearby:
                    # Apply the selected pattern with rotation
                    for dot_x, dot_y in selected_pattern:
                        # Rotate the pattern
                        rx, ry = rotate_point(dot_x - pattern_size//2, dot_y - pattern_size//2, pattern_rotation)
                        px = base_x + rx + pattern_size//2
                        py = base_y + ry + pattern_size//2
                        
                        if 0 <= px < width and 0 <= py < height:
                            # Vary intensity based on position
                            pos_var = ((px * py) % 20) - 10
                            final_intensity = max(130, min(190, pattern_intensity + pos_var))
                            pixels[px, py] = (final_intensity, final_intensity, final_intensity, 255)
    
    if 'density' in features:
        # Create a checkered gradient pattern
        cell_size = 10  # Smaller cells for more precision
        hex_values = [int(security_code[i:i+2], 16) for i in range(0, 6, 2)]
        
        # Pattern parameters from security code
        base_intensity = 220 + (hex_values[0] % 20)  # 220-240 base
        pattern_type = hex_values[1] % 4  # 4 different pattern types
        intensity_range = 10 + (hex_values[2] % 11)  # 10-20 range
        
        for y in range(0, height - cell_size, cell_size):
            for x in range(0, width - cell_size, cell_size):
                # Check if it's a white area away from QR code
                is_white_area = True
                has_qr_nearby = False
                
                for cy in range(cell_size):
                    for cx in range(cell_size):
                        px = x + cx
                        py = y + cy
                        if px >= width or py >= height:
                            continue
                        
                        r, g, b, a = pixels[px, py]
                        if r < 240 or g < 240 or b < 240:
                            is_white_area = False
                        if r < 50 and g < 50 and b < 50:
                            has_qr_nearby = True
                            break
                    if not is_white_area or has_qr_nearby:
                        break
                
                if is_white_area and not has_qr_nearby:
                    # Calculate pattern intensity based on position and type
                    if pattern_type == 0:
                        # Checkerboard
                        intensity_mod = intensity_range if (x//cell_size + y//cell_size) % 2 == 0 else 0
                    elif pattern_type == 1:
                        # Diagonal stripes
                        intensity_mod = intensity_range if (x + y) % (cell_size * 2) < cell_size else 0
                    elif pattern_type == 2:
                        # Radial
                        import math
                        dx = x - width/2
                        dy = y - height/2
                        dist = math.sqrt(dx*dx + dy*dy)
                        intensity_mod = int((math.cos(dist/20) + 1) * intensity_range/2)
                    else:
                        # Wavy pattern
                        import math
                        intensity_mod = int(math.sin(x/10) * math.cos(y/10) * intensity_range)
                    
                    # Apply the pattern
                    final_intensity = base_intensity - intensity_mod
                    for cy in range(cell_size):
                        for cx in range(cell_size):
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

@app.route('/')
def home():
    return render_template('index.html', version=VERSION)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        selected_features = data.get('features', [])
        
        # Generate a security code that will be used for both QRs
        security_code = secrets.token_hex(3)[:6]  # 6 hex chars
        
        # Combine text and security code (same for both QRs)
        combined_data = f"{text}|||{security_code}"
        print(f"Combined data: {combined_data}")  # Debug log
        
        # Create standard QR (with security code but no features)
        standard_qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=2,
        )
        standard_qr.add_data(combined_data)
        standard_qr.make(fit=True)
        standard_image = standard_qr.make_image(fill_color="black", back_color="white")
        
        # Convert standard QR to base64
        standard_buffered = io.BytesIO()
        standard_image.save(standard_buffered, format="PNG", quality=100)
        standard_base64 = base64.b64encode(standard_buffered.getvalue()).decode('utf-8')
        
        # Create secure QR (with security code AND features)
        secure_qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=2,
        )
        secure_qr.add_data(combined_data)
        secure_qr.make(fit=True)
        secure_image = secure_qr.make_image(fill_color="black", back_color="white")
        
        # Add security features only to secure QR
        if selected_features:
            secure_image = add_security_features(secure_image, selected_features, security_code)
        
        # Convert secure QR to base64
        secure_buffered = io.BytesIO()
        secure_image.save(secure_buffered, format="PNG", quality=100)
        secure_base64 = base64.b64encode(secure_buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'standard': {
                'image': standard_base64,
                'security_code': security_code,
                'features': []
            },
            'secure': {
                'image': secure_base64,
                'security_code': security_code,
                'features': selected_features
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/generate_secure_qr', methods=['POST'])
def generate_secure_qr():
    data = request.json
    text = data.get('text', '')
    security_code = data.get('security_code', '')
    
    if not text or not security_code:
        return jsonify({'error': 'Missing text or security code'}), 400
    
    try:
        # Create QR code with security features
        img = create_secure_qr(text, security_code)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'image': img_str})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_security_features', methods=['POST'])
def add_security_features_api():
    data = request.json
    image = data.get('image', '')
    features = data.get('features', [])
    security_code = data.get('security_code', '')
    
    if not image or not features or not security_code:
        return jsonify({'error': 'Missing image, features, or security code'}), 400
    
    try:
        # Load image from base64
        img = Image.open(io.BytesIO(base64.b64decode(image)))
        
        # Add security features
        img = add_security_features(img, features, security_code)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'image': img_str})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
