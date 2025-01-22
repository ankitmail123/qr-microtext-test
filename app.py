from flask import Flask, render_template, request, jsonify
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import os
import secrets
import numpy as np
import hashlib

VERSION = "1.2.1"
app = Flask(__name__)

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

def add_security_features(qr_image, features, security_code):
    # Convert to RGBA if not already
    if qr_image.mode != 'RGBA':
        qr_image = qr_image.convert('RGBA')
    
    width, height = qr_image.size
    draw = ImageDraw.Draw(qr_image)
    
    if 'micropattern' in features:
        # Generate unique micropattern points
        points = generate_pattern_points(security_code + "micro", width, height, 6)
        for x, y in points:
            if 0 <= x < width and 0 <= y < height and qr_image.getpixel((x, y))[0] > 200:
                # Add subtle dots with security-code-based opacity
                opacity = int(int(security_code[:2], 16) * 0.8)  # Use first 2 chars for opacity
                draw.point([x, y], fill=(0, 0, 0, opacity))
    
    if 'density' in features:
        # Generate unique density pattern points
        points = generate_pattern_points(security_code + "density", width, height, 12)
        for x, y in points:
            if 0 <= x < width and 0 <= y < height and qr_image.getpixel((x, y))[0] > 200:
                # Create a small pattern around each point
                pattern_opacity = int(int(security_code[2:4], 16) * 0.6)  # Use next 2 chars for opacity
                for dx, dy in [(1,1), (-1,-1), (1,-1), (-1,1)]:
                    px, py = x + dx, y + dy
                    if 0 <= px < width and 0 <= py < height:
                        draw.point([px, py], fill=(0, 0, 0, pattern_opacity))
    
    return qr_image

@app.route('/')
def home():
    return render_template('index.html', version=VERSION)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        features = data.get('features', ['micropattern', 'density'])
        
        # Generate a short security code (6 chars)
        security_code = secrets.token_hex(3)[:6]  # 6 hex chars
        
        # Combine text and security code
        combined_data = f"{text}|||{security_code}"
        
        # Create QR code optimized for small size
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,  # Small box size for 20mm output
            border=2,    # Minimal border
        )
        
        # Add data to QR code
        qr.add_data(combined_data)
        qr.make(fit=True)
        
        # Create QR code image with enhanced contrast
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Add security features
        qr_image = add_security_features(qr_image, features, security_code)
        
        # Convert to base64 for response
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG", quality=100)
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'image': qr_base64,
            'security_code': security_code,
            'version': VERSION,
            'features': features,
            'message': 'QR code generated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
