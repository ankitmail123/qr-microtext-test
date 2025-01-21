from flask import Flask, render_template, request, jsonify
from qr_generator import MicrotextQRGenerator
import base64
import io

app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

qr_generator = MicrotextQRGenerator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'No text provided'
            }), 400
            
        # Generate QR code
        qr_image = qr_generator.generate(text)
        
        # Convert to base64 for sending to frontend
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'status': 'success',
            'image': img_str
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
