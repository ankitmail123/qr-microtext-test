from flask import Flask, render_template, request, jsonify
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import os

app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '')
        
        # Create QR code with high error correction
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for response
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'image': qr_base64,
            'message': 'QR code generated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
