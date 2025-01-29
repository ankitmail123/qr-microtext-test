from app import create_secure_qr
from PIL import Image
import os
import json

def generate_test_patterns():
    """Generate QR codes with all pattern types for testing"""
    # Test cases with different patterns
    test_cases = [
        {
            "name": "X Pattern",
            "text": "12345",
            "security_code": "a1b2c3",
            "expected_pattern": "X",
            "expected_rotation": 90,
            "expected_intensity": 169
        },
        {
            "name": "Plus Pattern",
            "text": "12345",
            "security_code": "d4e5f6",
            "expected_pattern": "+",
            "expected_rotation": 45,
            "expected_intensity": 159
        },
        {
            "name": "9-Dot Pattern",
            "text": "12345",
            "security_code": "789abc",
            "expected_pattern": "9-dot",
            "expected_rotation": 135,
            "expected_intensity": 144
        },
        {
            "name": "Diamond Pattern",
            "text": "12345",
            "security_code": "def012",
            "expected_pattern": "diamond",
            "expected_rotation": 0,
            "expected_intensity": 175
        }
    ]
    
    # Create output directory
    os.makedirs("test_patterns", exist_ok=True)
    
    # Generate QR codes for each pattern
    for test_case in test_cases:
        print(f"\nGenerating {test_case['name']}:")
        print(f"- Text: {test_case['text']}")
        print(f"- Security Code: {test_case['security_code']}")
        print(f"- Expected Pattern: {test_case['expected_pattern']}")
        print(f"- Expected Rotation: {test_case['expected_rotation']}°")
        
        # Generate QR code
        qr = create_secure_qr(test_case['text'], test_case['security_code'])
        
        # Save with different quality settings
        for quality in ['high', 'medium', 'low']:
            output_path = f"test_patterns/{test_case['name'].lower().replace(' ', '_')}_{quality}.png"
            
            if quality == 'high':
                qr.save(output_path, format='PNG', optimize=False, compress_level=0)
            elif quality == 'medium':
                qr.save(output_path, format='PNG', optimize=True, compress_level=5)
            else:
                qr.save(output_path, format='PNG', optimize=True, compress_level=9)
            
            print(f"- Saved {quality} quality: {output_path}")
        
        # Save test case info
        info_path = f"test_patterns/{test_case['name'].lower().replace(' ', '_')}_info.json"
        with open(info_path, 'w') as f:
            json.dump(test_case, f, indent=2)
        print(f"- Saved info: {info_path}")

if __name__ == "__main__":
    generate_test_patterns()
