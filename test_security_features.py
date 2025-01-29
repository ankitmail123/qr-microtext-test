import pytest
from app import create_secure_qr, add_security_features
from PIL import Image
import io
import os
import numpy as np
import json

# Test cases
TEST_CASES = [
    {
        "name": "X Pattern",
        "security_code": "a1b2c3",
        "expected_pattern": "X",
        "expected_rotation": 90,
        "expected_intensity": 169
    },
    {
        "name": "Plus Pattern",
        "security_code": "d4e5f6",
        "expected_pattern": "+",
        "expected_rotation": 45,
        "expected_intensity": 159
    },
    {
        "name": "9-Dot Pattern",
        "security_code": "789abc",
        "expected_pattern": "9-dot",
        "expected_rotation": 135,
        "expected_intensity": 144
    },
    {
        "name": "Diamond Pattern",
        "security_code": "def012",
        "expected_pattern": "diamond",
        "expected_rotation": 0,
        "expected_intensity": 175
    }
]

@pytest.fixture(scope="module")
def test_output_dir():
    """Create test output directory"""
    os.makedirs("test_output", exist_ok=True)
    return "test_output"

def analyze_qr_image(image):
    """Analyze QR code image for security features"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    width, height = image.size
    pixels = image.load()
    
    # Initialize counters
    pixel_ranges = {
        'black': 0,  # < 50
        'pattern': 0,  # 130-190
        'density': 0,  # 220-240
        'white': 0  # > 240
    }
    
    # Count pixels in each range
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r < 50:
                pixel_ranges['black'] += 1
            elif 130 <= r <= 190:
                pixel_ranges['pattern'] += 1
            elif 220 <= r <= 240:
                pixel_ranges['density'] += 1
            elif r > 240:
                pixel_ranges['white'] += 1
    
    total_pixels = width * height
    return {
        'total_pixels': total_pixels,
        'counts': pixel_ranges,
        'percentages': {k: (v/total_pixels)*100 for k, v in pixel_ranges.items()}
    }

def detect_pattern_type(image, expected_intensity):
    """Detect the type of security pattern in the image"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    width, height = image.size
    pixels = image.load()
    
    # Define pattern templates
    patterns = {
        'X': [(0,0), (0,4), (1,1), (1,3), (2,2), (3,1), (3,3), (4,0), (4,4)],
        '+': [(0,2), (1,2), (2,0), (2,1), (2,2), (2,3), (2,4), (3,2), (4,2)],
        '9-dot': [(0,0), (0,2), (0,4), (2,0), (2,2), (2,4), (4,0), (4,2), (4,4)],
        'diamond': [(0,1), (0,3), (1,0), (1,4), (2,2), (3,0), (3,4), (4,1), (4,3)]
    }
    
    pattern_matches = {k: 0 for k in patterns.keys()}
    pattern_size = 5
    pattern_spacing = 20
    
    # Scan for patterns
    for base_y in range(pattern_size, height - pattern_size, pattern_spacing):
        for base_x in range(pattern_size, width - pattern_size, pattern_spacing):
            # Check each pattern template
            for pattern_name, template in patterns.items():
                matches = 0
                total_points = len(template)
                
                for px, py in template:
                    x = base_x + px
                    y = base_y + py
                    if 0 <= x < width and 0 <= y < height:
                        r, g, b = pixels[x, y]
                        if abs(r - expected_intensity) <= 15:  # Allow some variation
                            matches += 1
                
                if matches/total_points > 0.7:  # 70% match threshold
                    pattern_matches[pattern_name] += 1
    
    # Return the most frequently detected pattern
    if any(pattern_matches.values()):
        return max(pattern_matches.items(), key=lambda x: x[1])[0]
    return None

@pytest.mark.parametrize("test_case", TEST_CASES)
def test_qr_generation(test_case, test_output_dir):
    """Test QR code generation with different security patterns"""
    # Generate QR code
    test_text = "12345"
    qr = create_secure_qr(test_text, test_case["security_code"])
    
    # Save for manual inspection
    output_path = os.path.join(test_output_dir, f"qr_{test_case['name'].lower().replace(' ', '_')}.png")
    qr.save(output_path, format='PNG', optimize=False, compress_level=0)
    
    # Analyze the image
    analysis = analyze_qr_image(qr)
    
    # Basic security feature checks
    assert analysis['counts']['pattern'] > 100, "Should have sufficient pattern pixels"
    assert analysis['counts']['density'] > 100, "Should have sufficient density variation pixels"
    
    # Pattern type check
    detected_pattern = detect_pattern_type(qr, test_case["expected_intensity"])
    assert detected_pattern == test_case["expected_pattern"], f"Expected {test_case['expected_pattern']} pattern"
    
    # Save analysis results
    results = {
        "test_case": test_case["name"],
        "security_code": test_case["security_code"],
        "pixel_analysis": analysis,
        "detected_pattern": detected_pattern
    }
    
    results_path = os.path.join(test_output_dir, f"analysis_{test_case['name'].lower().replace(' ', '_')}.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

@pytest.mark.parametrize("test_case", TEST_CASES)
def test_density_variations(test_case):
    """Test density variation patterns"""
    test_text = "12345"
    qr = create_secure_qr(test_text, test_case["security_code"])
    analysis = analyze_qr_image(qr)
    
    # Check density variation percentages
    assert analysis['percentages']['density'] > 5, "Should have at least 5% density variation pixels"
    assert analysis['percentages']['density'] < 15, "Should have less than 15% density variation pixels"

@pytest.mark.parametrize("test_case", TEST_CASES)
def test_pattern_preservation(test_case, test_output_dir):
    """Test if patterns are preserved after saving and loading"""
    test_text = "12345"
    qr = create_secure_qr(test_text, test_case["security_code"])
    
    # Test different quality settings
    quality_settings = [
        ('high', {'optimize': False, 'compress_level': 0}),
        ('medium', {'optimize': True, 'compress_level': 5}),
        ('low', {'optimize': True, 'compress_level': 9})
    ]
    
    for quality, settings in quality_settings:
        output_path = os.path.join(test_output_dir, f"qr_{test_case['name'].lower()}_{quality}.png")
        qr.save(output_path, format='PNG', **settings)
        
        # Load and analyze
        loaded_qr = Image.open(output_path)
        analysis = analyze_qr_image(loaded_qr)
        
        # Verify patterns are preserved
        assert analysis['counts']['pattern'] > 100, f"Patterns should be preserved in {quality} quality"
        assert analysis['counts']['density'] > 100, f"Density variations should be preserved in {quality} quality"
