import os
import json
import base64
from PIL import Image
import qrcode
from app import create_secure_qr, add_security_features

def generate_test_cases():
    test_cases = [
        {
            "text": "Hello World! This is test case 1",
            "security_code": "a1b2c3"
        },
        {
            "text": "https://example.com/test/case/2",
            "security_code": "d4e5f6"
        },
        {
            "text": "Test Case 3: Special Characters !@#$%",
            "security_code": "789abc"
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases):
        print(f"\nTesting Case {i+1}:")
        print(f"Text: {case['text']}")
        print(f"Security Code: {case['security_code']}")
        
        # Generate standard QR
        standard_qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        standard_qr.add_data(case['text'])
        standard_qr.make(fit=True)
        standard_img = standard_qr.make_image(fill_color="black", back_color="white")
        
        # Save standard QR
        standard_path = f"test_standard_qr_{i+1}.png"
        standard_img.save(standard_path)
        print(f"Generated standard QR: {standard_path}")
        
        # Generate secure QR
        secure_img = create_secure_qr(case['text'], case['security_code'])
        secure_path = f"test_secure_qr_{i+1}.png"
        secure_img.save(secure_path)
        print(f"Generated secure QR: {secure_path}")
        
        # Convert images to base64 for testing
        def image_to_base64(img_path):
            with open(img_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        
        standard_b64 = image_to_base64(standard_path)
        secure_b64 = image_to_base64(secure_path)
        
        results.append({
            "case_number": i + 1,
            "text": case['text'],
            "security_code": case['security_code'],
            "standard_qr": standard_b64,
            "secure_qr": secure_b64
        })
    
    # Save test cases for the scanner
    with open('test_cases.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nGenerated test cases and saved to test_cases.json")
    print("Run the scanner test to verify security feature detection")

if __name__ == "__main__":
    generate_test_cases()
