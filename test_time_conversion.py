#!/usr/bin/env python3
"""
Test script for Luxembourgish time conversion functionality
"""

from luxembourgish_normalizer import LuxembourgishNormalizer

def test_time_conversions():
    """Test the time converter with various time formats"""
    normalizer = LuxembourgishNormalizer()
    
    test_times = [
        # HH:MM format
        "10:34",
        "09:07", 
        "17:58",
        "00:00",
        "12:30",
        "23:59",
        "01:05",
        "15:45",
        
        # HHhMM format
        "10h34",
        "09h07",
        "17h58", 
        "00h00",
        "12h30",
        "23h59",
        "01h05",
        "15h45",
        
        # Mixed text with times
        "D'Meeting ass um 10:34",
        "D'Zuch kënnt um 17h58",
        "Mir treffen eis um 09:07",
        "D'Geschäft ass zou um 23:59"
    ]
    
    print("=== LUXEMBOURGISH TIME CONVERSIONS ===")
    print("=" * 50 + "\n")
    
    for time_str in test_times:
        result = normalizer.normalize_times(time_str)
        print(f"Input:  {time_str}")
        print(f"Output: {result}")
        print()

def test_time_in_context():
    """Test time conversion within larger text"""
    normalizer = LuxembourgishNormalizer()
    
    test_texts = [
        "RTL|Update: 09.07.2025 17:58|10 Commentaire(n)",
        "Céline Eischen|Update: 09.07.2025 17:41|0 Commentaire(n)",
        "tIM mORIZET|Update: 09.07.2025 16:09",
        "D'Meeting ass um 10:34 an d'Geschäft ass zou um 23:59",
        "Mir treffen eis um 09h07 fir d'Projet ze besprechen"
    ]
    
    print("=== TIME CONVERSIONS IN CONTEXT ===")
    print("=" * 50 + "\n")
    
    for text in test_texts:
        result = normalizer.normalize(text)
        print(f"Input:  {text}")
        print(f"Output: {result}")
        print()

if __name__ == "__main__":
    test_time_conversions()
    test_time_in_context() 