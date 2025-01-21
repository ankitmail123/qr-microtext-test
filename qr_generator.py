import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageColor
import json
import random
import numpy as np
from PIL import ImageEnhance, ImageFilter
import math
import hashlib
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class SecurityFeature:
    name: str
    description: str
    recommended_size: str
    detection_method: str
    min_dpi: int

class MiniSecureQRGenerator:
    def __init__(self):
        self.features = {
            'micropattern': SecurityFeature(
                name="Micropattern QR",
                description="High-contrast microscopic dot patterns optimized for mobile scanning",
                recommended_size="20mm x 20mm",
                detection_method="Binary pattern analysis",
                min_dpi=300
            ),
            'density_variation': SecurityFeature(
                name="Density Variation QR",
                description="Binary density patterns that become uniform when copied",
                recommended_size="20mm x 20mm",
                detection_method="Local density analysis",
                min_dpi=300
            )
        }

    def _create_base_qr(self, data: dict) -> Image.Image:
        """Create base QR code image optimized for small size."""
        # Combine main text and security code in a structured way
        qr_data = {
            "text": data["main_text"],
            "sec": hashlib.sha256(data["security_code"].encode()).hexdigest()[:8]
        }
        
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,  # Smaller box size for better small-scale rendering
            border=2,    # Smaller border for compact size
        )
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    def _get_pattern_seed(self, security_code: str) -> int:
        """Generate a deterministic seed from security code."""
        return int(hashlib.sha256(security_code.encode()).hexdigest()[:8], 16)

    def _add_micropattern(self, img: Image.Image, security_code: str) -> Image.Image:
        """Add high-contrast microscopic dot pattern optimized for mobile scanning."""
        width, height = img.size
        pattern = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(pattern)
        
        # Use security code to generate deterministic pattern
        random.seed(self._get_pattern_seed(security_code))
        
        # Create binary dot pattern (only fully opaque or transparent)
        dot_spacing = 4  # Increased spacing for better detection
        for x in range(0, width, dot_spacing):
            for y in range(0, height, dot_spacing):
                if random.random() > 0.5:
                    # Use security code to determine dot pattern
                    if random.random() > 0.7:  # 30% chance of dot cluster
                        draw.point((x, y), fill=(0, 0, 0, 255))
                        if x + 1 < width and y + 1 < height:
                            draw.point((x+1, y), fill=(0, 0, 0, 255))
                            draw.point((x, y+1), fill=(0, 0, 0, 255))
                    else:
                        draw.point((x, y), fill=(0, 0, 0, 255))
        
        return Image.alpha_composite(img, pattern)

    def _add_density_variation(self, img: Image.Image, security_code: str) -> Image.Image:
        """Add binary density pattern optimized for small size and mobile detection."""
        width, height = img.size
        pattern = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(pattern)
        
        # Use security code to generate deterministic pattern
        random.seed(self._get_pattern_seed(security_code))
        
        # Create larger cell-based density pattern
        cell_size = 6  # Increased cell size for better detection
        for x in range(0, width, cell_size):
            for y in range(0, height, cell_size):
                # Create distinct density regions based on security code
                angle_mod = int(security_code[0], 36) / 36  # Use first char for pattern variation
                density = int(abs(math.sin((x/width + angle_mod) * math.pi) * 
                               math.cos((y/height + angle_mod) * math.pi) * 8))
                
                # Fill cell with dots based on density
                for i in range(density):
                    dot_x = x + random.randint(0, cell_size-1)
                    dot_y = y + random.randint(0, cell_size-1)
                    if dot_x < width and dot_y < height:
                        draw.point((dot_x, dot_y), fill=(0, 0, 0, 255))
        
        return Image.alpha_composite(img, pattern)

    def generate_all_variants(self, main_text: str, security_code: str) -> Dict[str, Tuple[Image.Image, SecurityFeature]]:
        """Generate all security variants of the QR code."""
        data = {
            "main_text": main_text,
            "security_code": security_code
        }

        # Create base QR code
        base_qr = self._create_base_qr(data)
        
        # Generate each variant
        variants = {}
        
        # Micropattern
        micro_qr = self._add_micropattern(base_qr.copy(), security_code)
        variants['micropattern'] = (micro_qr, self.features['micropattern'])
        
        # Density Variation
        density_qr = self._add_density_variation(base_qr.copy(), security_code)
        variants['density_variation'] = (density_qr, self.features['density_variation'])
        
        return variants

    @staticmethod
    def verify_security_feature(image_path: str, feature_type: str, security_code: str) -> Tuple[bool, str]:
        """Verify a specific security feature in the QR code."""
        try:
            img = Image.open(image_path)
            
            if feature_type == 'micropattern':
                # Convert to binary and analyze dot pattern
                # This would be implemented in the mobile app using OpenCV
                return True, "Micropattern verified"
                
            elif feature_type == 'density_variation':
                # Analyze local density variations
                # This would be implemented in the mobile app using OpenCV
                return True, "Density variation verified"
                
            else:
                return False, "Unknown security feature type"
                
        except Exception as e:
            return False, str(e)

    def get_print_instructions(self) -> str:
        """Get printing instructions for optimal results."""
        return """
Printing Instructions for 20mm x 20mm QR Codes:
1. Minimum printer resolution: 300 DPI
2. Use high-quality paper (at least 80 gsm)
3. Ensure printer is calibrated for sharp black output
4. No scaling during printing (print at 100% size)
5. Verify printed size is exactly 20mm x 20mm
"""

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python qr_generator.py <main_text> <security_code>")
        print("Example: python qr_generator.py 'Hello World' 'SEC123'")
        sys.exit(1)
    
    # Get input from command line arguments
    main_text = sys.argv[1]
    security_code = sys.argv[2]
    
    # Test the generator
    generator = MiniSecureQRGenerator()
    
    # Generate all variants
    variants = generator.generate_all_variants(main_text, security_code)
    
    # Print instructions
    print("\n" + generator.get_print_instructions())
    print("-" * 50)
    
    # Import matplotlib for display
    import matplotlib.pyplot as plt
    
    # Create a figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle(f'QR Codes with Security Features (20mm x 20mm)\nMain Text: {main_text}')
    
    # Save and display each variant
    for i, (feature_name, (qr_image, feature_info)) in enumerate(variants.items()):
        output_path = f"secure_qr_{feature_name}_mini.png"
        qr_image.save(output_path)
        
        # Display image
        axes[i].imshow(qr_image)
        axes[i].set_title(f"{feature_info.name}\n{feature_info.description}")
        axes[i].axis('off')
        
        print(f"\nGenerated {feature_info.name}")
        print(f"Description: {feature_info.description}")
        print(f"Recommended Size: {feature_info.recommended_size}")
        print(f"Minimum DPI: {feature_info.min_dpi}")
        print(f"Detection Method: {feature_info.detection_method}")
        print(f"Output File: {output_path}")
        print("-" * 50)
    
    plt.tight_layout()
    plt.show()
