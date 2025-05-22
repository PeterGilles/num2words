#!/usr/bin/env python3
"""
Test script for advanced Luxembourgish number conversion
Includes special cases like:
- Years with 'er' suffix (e.g., '1970er')
- Units with or without spaces (e.g., '90°', '100 ml', '50ml')
"""

import re
import sys
import os

# Add the parent directory to the path so we can import our module
sys.path.insert(0, os.path.abspath('..'))

try:
    from num2words.lang_LB import Num2Word_LB
except ImportError:
    try:
        from lang_LB import Num2Word_LB
    except ImportError:
        print("ERROR: Could not import Num2Word_LB class")
        sys.exit(1)

class TextNormalizer:
    """Text normalizer for Luxembourgish with special handling for years, units, etc."""
    
    def __init__(self):
        self.lb = Num2Word_LB()
        
        # Unit mappings
        self.unit_mappings = {
            '°': 'Grad',
            'ml': 'Milliliter',
            'gr': 'Gramm',
            '%': 'Prozent'
        }

    def normalize_years_with_suffix(self, text):
        """
        Convert expressions like '1970er' to 'nonnzénghonnertsiwenzeger'.
        Matches year patterns followed by 'er' suffix.
        """
        # Pattern for years between 1000-2099 followed by 'er'
        pattern = r'\b(1\d{3}|20\d{2})er\b'
        
        def replace_year_with_suffix(match):
            year = int(match.group(1))
            # Convert the year to words using the to_year method if available
            try:
                year_text = self.lb.to_year(year)
            except AttributeError:
                # Fallback if to_year method is not available
                year_text = self.lb.to_cardinal(year)
            
            # Add the -er suffix
            return f"{year_text}er"
        
        # Replace all occurrences in the text
        result = re.sub(pattern, replace_year_with_suffix, text)
        return result

    def normalize_units(self, text):
        """
        Convert numbers followed by units like °, ml, gr, or %
        with or without spaces (e.g., '90°', '100 ml', '50ml').
        """
        # Handle each unit type separately to ensure they all match properly
        
        # Handle temperature (°)
        temp_pattern = r'\b(\d+)\s*°\b'
        text = re.sub(temp_pattern, lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Grad", text)
        
        # Handle milliliters (ml)
        ml_pattern = r'\b(\d+)\s*ml\b'
        text = re.sub(ml_pattern, lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Milliliter", text)
        
        # Handle grams (gr)
        gr_pattern = r'\b(\d+)\s*gr\b'
        text = re.sub(gr_pattern, lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Gramm", text)
        
        # Handle percentages (%)
        percent_pattern = r'\b(\d+)\s*%\b'
        text = re.sub(percent_pattern, lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Prozent", text)
        
        # Fix any singular forms (1 unit)
        text = text.replace("eent Milliliter", "een Milliliter")
        text = text.replace("eent Gramm", "een Gramm")
        text = text.replace("eent Grad", "een Grad")
        text = text.replace("eent Prozent", "een Prozent")
        
        return text
        
    def normalize_text(self, text):
        """Apply all normalization rules to the text"""
        # First normalize years with suffix
        result = self.normalize_years_with_suffix(text)
        
        # Then normalize units
        result = self.normalize_units(result)
        
        # Return the fully normalized text
        return result


def test_normalizer():
    """Test the text normalizer with various examples"""
    normalizer = TextNormalizer()
    
    # Test cases
    test_cases = [
        # Years with suffix
        "1970er", "1980er", "1990er", "2000er", "2020er",
        "In den 1970er bis 1990er Jahren",
        
        # Units - temperature
        "90°", "21°", "0°", "100°",
        "Et ass 30° haut",
        
        # Units - volume with/without space
        "1ml", "50 ml", "100ml", "500 ml", "1000ml",
        "Eng Fläsch vun 750ml",
        
        # Units - weight with/without space
        "1gr", "50 gr", "100gr", "500 gr", "1000gr",
        "D'Paquet weit 500gr",
        
        # Units - percentage with/without space
        "10%", "25 %", "50%", "100 %",
        "Eng Erhéijung vun 10%",
        
        # Mixed examples
        "1970er: 90° an 500ml Waasser mat 50gr Miel an 25% Zocker",
        "2000er: Eng Fläsch vun 750ml an 1kg Miel",
        "Am 1985er Wanter waren et -10°"
    ]
    
    print("=== TESTING LUXEMBOURGISH TEXT NORMALIZATION ===")
    print("=" * 50 + "\n")
    
    for test in test_cases:
        result = normalizer.normalize_text(test)
        print(f"Input:  {test}")
        print(f"Output: {result}")
        print()


def main():
    """Run all tests"""
    test_normalizer()
    print("Tests completed.")


if __name__ == "__main__":
    main()