#!/usr/bin/env python3
"""
Test script for Luxembourgish date conversions using num2words
"""

import re
import sys
from num2words.lang_LB import Num2Word_LB

class DateConverter:
    """Convert dates to Luxembourgish text"""
    
    def __init__(self):
        self.lb = Num2Word_LB()
        
        # Month mappings
        self.months = {
            'januar': 'Januar',
            'februar': 'Februar', 
            'mäerz': 'Mäerz',
            'abrëll': 'Abrëll',
            'mee': 'Mee',
            'juni': 'Juni',
            'juli': 'Juli',
            'august': 'August',
            'september': 'September',
            'oktober': 'Oktober',
            'november': 'November',
            'dezember': 'Dezember'
        }

    def adjust_ordinal_for_following_word(self, ordinal, following_word):
        """
        Adjust the ordinal ending based on the following word.
        Drop final 'n' if the following word doesn't start with vowel or n, d, t, z.
        """
        if not following_word:
            return ordinal
        
        # Get the first letter of the following word
        first_letter = following_word[0].lower()
        
        # Keep 'n' if following word starts with vowel or n, d, t, z
        if first_letter in 'aeiouäëöündtz':
            return ordinal
        
        # Drop final 'n' if it exists
        if ordinal.endswith('n'):
            return ordinal[:-1]
        
        return ordinal

    def convert_date(self, date_str):
        """
        Convert date string to Luxembourgish text
        Handles various formats:
        - 30. Abrëll 2010
        - den 30. Abrëll 2010
        - de 15. Mee 1982
        - um 5. Juli 2021
        - 21. Januar 1467
        - 28.11.1733
        - 5. Juli 2021
        - 3.3.1844
        - Mäerz 1756 (without day)
        - 6. 6.7.1940 (double day format)
        """
        
        # Clean up the input
        date_str = date_str.strip()
        
        # Extract article if present
        article = ""
        if date_str.startswith("den "):
            article = "den "
            date_str = date_str[4:]  # Remove "den "
        elif date_str.startswith("de "):
            article = "de "
            date_str = date_str[3:]  # Remove "de "
        elif date_str.startswith("um "):
            article = "um "
            date_str = date_str[3:]  # Remove "um "
        
        # Handle double day format like "6. 6.7.1940"
        if re.match(r'\d+\.\s+\d+\.\d+\.\d+', date_str):
            # Remove the first day number
            date_str = re.sub(r'^\d+\.\s+', '', date_str)
        
        # Pattern for dates with day, month, year
        pattern1 = r'(\d+)\.\s*([A-Za-zäëöüÄËÖÜ]+)\s+(\d{4})'
        match1 = re.match(pattern1, date_str)
        
        if match1:
            day = int(match1.group(1))
            month = match1.group(2).lower()
            year = int(match1.group(3))
            
            # Convert day to ordinal
            day_ordinal = self.lb.to_ordinal(day)
            
            # Get month name
            month_name = self.months.get(month, month.capitalize())
            
            # Adjust ordinal based on the following month name
            day_ordinal = self.adjust_ordinal_for_following_word(day_ordinal, month_name)
            
            # Convert year
            year_text = self.lb.to_year(year)
            
            return f"{article}{day_ordinal} {month_name} {year_text}"
        
        # Pattern for dates with day.month.year format
        pattern2 = r'(\d+)\.(\d+)\.(\d{4})'
        match2 = re.match(pattern2, date_str)
        
        if match2:
            day = int(match2.group(1))
            month_num = int(match2.group(2))
            year = int(match2.group(3))
            
            # Convert day to ordinal
            day_ordinal = self.lb.to_ordinal(day)
            
            # Get month name from number
            month_names = list(self.months.values())
            if 1 <= month_num <= 12:
                month_name = month_names[month_num - 1]
            else:
                month_name = f"Monat {month_num}"
            
            # Adjust ordinal based on the following month name
            day_ordinal = self.adjust_ordinal_for_following_word(day_ordinal, month_name)
            
            # Convert year
            year_text = self.lb.to_year(year)
            
            return f"{article}{day_ordinal} {month_name} {year_text}"
        
        # Pattern for dates with only month and year
        pattern3 = r'([A-Za-zäëöüÄËÖÜ]+)\s+(\d{4})'
        match3 = re.match(pattern3, date_str)
        
        if match3:
            month = match3.group(1).lower()
            year = int(match3.group(2))
            
            # Get month name
            month_name = self.months.get(month, month.capitalize())
            
            # Convert year
            year_text = self.lb.to_year(year)
            
            return f"{article}{month_name} {year_text}"
        
        # Pattern for dates with day.month.year (short format)
        pattern4 = r'(\d+)\.(\d+)\.(\d{4})'
        match4 = re.match(pattern4, date_str)
        
        if match4:
            day = int(match4.group(1))
            month_num = int(match4.group(2))
            year = int(match4.group(3))
            
            # Convert day to ordinal
            day_ordinal = self.lb.to_ordinal(day)
            
            # Get month name from number
            month_names = list(self.months.values())
            if 1 <= month_num <= 12:
                month_name = month_names[month_num - 1]
            else:
                month_name = f"Monat {month_num}"
            
            # Adjust ordinal based on the following month name
            day_ordinal = self.adjust_ordinal_for_following_word(day_ordinal, month_name)
            
            # Convert year
            year_text = self.lb.to_year(year)
            
            return f"{article}{day_ordinal} {month_name} {year_text}"
        
        return f"Could not parse: {date_str}"

def test_dates():
    """Test the date converter with the provided dates"""
    converter = DateConverter()
    
    test_dates = [
        "den 30. Abrëll 2010",
        "den 21. Januar 1467", 
        "de 15. Mee 1982",
        "den 28.11.1733",
        "um 5. Juli 2021",
        "den 3.3.1844",
        "den 24. Dezember 1965",
        "de 14.10.1999",
        "5. Februar 2020",
        "5.8.1501",
        "30. September 1918",
        "11.6.2003",
        "Mäerz 1756",
        "30.4.2018",
        "Oktober 1344",
        "8.2.2015",
        "Abrëll 1887",
        "16.6.1492",
        "2. Mee 2022",
        "6. 6.7.1940",
        "Januar 1977",
        "21.10.1855",
        "2. Mäerz 1604",
        "10.8.2013",
        "1. Dezember 1541",
        "9.9.1990",
        "4. Juli 1802",
        "18.2.2024",
        "23. Oktober 1699",
        "31.3.2011",
        "4. Mee 1575",
        "2.11.1900",
        "10. Februar 1432",
        "12.12.2012",
        "2. Abrëll 1950",
        "7.6.1717",
        "15. Oktober 2004",
        "14.1.1744",
        "19. Mäerz 2019",
        "1.5.1866"
    ]
    
    print("=== LUXEMBOURGISH DATE CONVERSIONS (WITH ORDINAL ADJUSTMENT) ===")
    print("=" * 60 + "\n")
    
    for date_str in test_dates:
        result = converter.convert_date(date_str)
        print(f"Input:  {date_str}")
        print(f"Output: {result}")
        print()

if __name__ == "__main__":
    test_dates() 