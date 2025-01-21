from flask import Flask, render_template, request, jsonify
from qr_generator import MiniSecureQRGenerator
import base64
import io
import secrets

app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

qr_generator = MiniSecureQRGenerator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    try:
        data = request.json
        text = data.get('text', '')
        security_code = data.get('security_code', secrets.token_hex(4))  # Generate random if not provided
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'No text provided'
            }), 400
            
        # Generate QR codes with security features
        variants = qr_generator.generate_all_variants(text, security_code)
        
        # Convert all variants to base64
        images = {}
        for feature_name, (qr_image, feature_info) in variants.items():
            buffered = io.BytesIO()
            qr_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            images[feature_name] = {
                'image': img_str,
                'name': feature_info.name,
                'description': feature_info.description,
                'recommended_size': feature_info.recommended_size,
                'min_dpi': feature_info.min_dpi,
                'detection_method': feature_info.detection_method
            }
        
        return jsonify({
            'status': 'success',
            'security_code': security_code,  # Return the security code used
            'images': images,
            'print_instructions': qr_generator.get_print_instructions()
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
