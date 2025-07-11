#!/usr/bin/env python3
"""
Debug script for phone number normalization
"""

from luxembourgish_normalizer import LuxembourgishNormalizer
import re

def test_phone_debug():
    normalizer = LuxembourgishNormalizer()
    
    test_phone_lines = [
        "Telefon: 62 11 08.",
        "Telefon: 08",
        "Telefon: 62 11 08",
        "Telefon: 62 11 08",
        "08",
        "62 11 08"
    ]
    
    print("=== PHONE NUMBER DEBUG ===")
    print("=" * 30 + "\n")
    
    for line in test_phone_lines:
        print(f"Input:  '{line}'")
        
        # Debug: show what groups are found
        groups = re.findall(r'\b\d{2,}\b', line)
        print(f"Groups found: {groups}")
        
        # Test the phone normalization
        result = normalizer.normalize_phone_numbers(line)
        print(f"Output: '{result}'")
        print()

if __name__ == "__main__":
    test_phone_debug() 