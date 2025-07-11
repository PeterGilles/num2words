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
        Convert expressions like '1970er' to 'nonzénghonnertsiwenzeger' and '80er' to 'achtzeger'.
        Matches year patterns followed by 'er' suffix.
        """
        # Pattern for years between 1000-2099 followed by 'er'
        year_pattern = r'\b(1\d{3}|20\d{2})er\b'
        
        # Pattern for 2-digit numbers followed by 'er'
        decade_pattern = r'\b([1-9]\d)er\b'
        
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
        
        def replace_decade_with_suffix(match):
            decade = int(match.group(1))
            # Convert the decade to words
            decade_text = self.lb.to_cardinal(decade)
            # Add the -er suffix
            return f"{decade_text}er"
        
        # First replace 4-digit years
        result = re.sub(year_pattern, replace_year_with_suffix, text)
        # Then replace 2-digit decades
        result = re.sub(decade_pattern, replace_decade_with_suffix, result)
        
        return result

    def normalize_units(self, text):
        """
        Convert numbers followed by units like °, ml, gr, kg, or %
        with or without spaces (e.g., '90°', '100 ml', '50ml', '1kg').
        """
        # Handle negative temperatures first
        neg_temp_pattern = r'(?<![0-9])-(\d+)\s*[°\u00B0]'
        text = re.sub(neg_temp_pattern, lambda m: f"minus {self.lb.to_cardinal(int(m.group(1)))} Grad", text)
        
        # Patch: Use 'eenhonnert' for 100 when followed by a unit (°/ml/gr/kg)
        def cardinal_for_unit(num):
            if int(num) == 1:
                return "een"
            if int(num) == 100:
                return "eenhonnert"
            return self.lb.to_cardinal(int(num))

        # Handle temperature (°)
        temp_pattern = r'(?<![0-9])(\d+)\s*[°\u00B0]'
        text = re.sub(temp_pattern, lambda m: f"{cardinal_for_unit(m.group(1))} Grad", text)
        
        # Handle milliliters (ml)
        ml_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*ml\b'
        text = re.sub(ml_pattern, lambda m: f"{cardinal_for_unit(m.group(1))} Milliliter", text)
        
        # Handle grams (gr)
        gr_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*gr\b'
        text = re.sub(gr_pattern, lambda m: f"{cardinal_for_unit(m.group(1))} Gramm", text)
        
        # Handle kilograms (kg)
        kg_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*kg\b'
        text = re.sub(kg_pattern, lambda m: f"{'ee' if int(m.group(1)) == 1 else cardinal_for_unit(m.group(1))} Kilogramm", text)
        
        # Handle percentages (%)
        percent_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*%'
        text = re.sub(percent_pattern, lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Prozent", text)
        
        # Fix any singular forms (1 unit)
        text = text.replace("eent Milliliter", "een Milliliter")
        text = text.replace("eent Gramm", "een Gramm")
        text = text.replace("eent Grad", "een Grad")
        text = text.replace("eent Prozent", "een Prozent")
        
        return text

    def normalize_currency(self, text):
        """
        Convert currency expressions like '1,50 EUR', '1.50 €', '2,25 USD' to Luxembourgish text.
        Handles both comma and dot as decimal separators.
        """
        # Pattern for currency expressions: number followed by currency code or symbol
        # Supports both comma and dot as decimal separators
        currency_pattern = r'(\d+[,.]\d+)\s*(EUR|€|USD|\$|GBP|£|CNY|¥|DEM|DM)'
        
        def replace_currency(match):
            amount_str = match.group(1)
            currency = match.group(2)
            
            # Convert comma to dot for parsing
            if ',' in amount_str:
                amount_str = amount_str.replace(',', '.')
            
            try:
                amount = float(amount_str)
                
                # Map currency symbols to currency codes
                currency_map = {
                    '€': 'EUR',
                    '$': 'USD', 
                    '£': 'GBP',
                    '¥': 'CNY',
                    'DM': 'DEM'
                }
                
                currency_code = currency_map.get(currency, currency)
                
                # Convert to Luxembourgish currency text
                return self.lb.to_currency(amount, currency_code)
                
            except ValueError:
                # If parsing fails, return original
                return match.group(0)
        
        return re.sub(currency_pattern, replace_currency, text)
        
    def fix_final_n(self, text):
        """
        Fixes words ending in '-en' to keep or drop the final 'n' based on the next word.
        The 'n' is kept only if the next word starts with a vowel (aeiouäöü) or n, d, t, z, h (not case-sensitive).
        """
        # Regex: word ending in 'en' followed by a space and a word
        pattern = re.compile(r'(\ben)(\s+)([a-zA-ZäöüÄÖÜ])', re.UNICODE)
        def repl(match):
            en = match.group(1)
            space = match.group(2)
            next_char = match.group(3)
            if next_char.lower() in 'aeiouäöünndtzh':
                return en + space + next_char
            else:
                return 'e' + space + next_char
        # Apply repeatedly in case of multiple matches
        prev = None
        while prev != text:
            prev = text
            text = pattern.sub(repl, text)
        return text

    def normalize_text(self, text):
        """Apply all normalization rules to the text"""
        # First normalize years with suffix
        result = self.normalize_years_with_suffix(text)
        
        # Then normalize currency
        result = self.normalize_currency(result)
        
        # Then normalize units
        result = self.normalize_units(result)
        
        # Then fix final n
        result = self.fix_final_n(result)
        
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
        # Decade only
        "80er",
        
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


def test_ordinals():
    lb = Num2Word_LB()
    cases = [
        (100, "honnertsten"),
        (101, "eenhonnertéischten"),
        (102, "eenhonnertzweeten"),
        (103, "eenhonnertdrëtten"),
        (104, "eenhonnertvéierten"),
        (105, "eenhonnertfënneften"),
        (106, "eenhonnertsechsten"),
        (107, "eenhonnertsiwenten"),
        (108, "eenhonnertaachten"),
        (109, "eenhonnertnéngten"),
        (110, "eenhonnerzéngten"),
        (111, "eenhonnerteeleften"),
        (200, "zweehonnertsten"),
        (201, "zweehonnertéischten"),
        (202, "zweehonnertzweeten"),
        (203, "zweehonnertdrëtten"),
        (204, "zweehonnertvéierten"),
        (205, "zweehonnertfënneften"),
        (206, "zweehonnertsechsten"),
        (207, "zweehonnertsiwenten"),
        (208, "zweehonnertaachten"),
        (209, "zweehonnertnéngten"),
        (210, "zweehonnerzéngten"),
        (211, "zweehonnerteeleften"),
        (300, "dräihonnertsten"),
        (301, "dräihonnertéischten"),
        (302, "dräihonnertzweeten"),
        (303, "dräihonnertdrëtten"),
        (304, "dräihonnertvéierten"),
        (305, "dräihonnertfënneften"),
        (306, "dräihonnertsechsten"),
        (307, "dräihonnertsiwenten"),
        (308, "dräihonnertaachten"),
        (309, "dräihonnertnéngten"),
        (310, "dräihonnerzéngten"),
        (311, "dräihonnerteeleften"),
        (400, "véierhonnertsten"),
        (401, "véierhonnertéischten"),
        (402, "véierhonnertzweeten"),
        (403, "véierhonnertdrëtten"),
        (404, "véierhonnertvéierten"),
        (405, "véierhonnertfënneften"),
        (406, "véierhonnertsechsten"),
        (407, "véierhonnertsiwenten"),
        (408, "véierhonnertaachten"),
        (409, "véierhonnertnéngten"),
        (410, "véierhonnertzéngten"),
        (411, "véierhonnerteeleften"),
        (500, "fënnefhonnertsten"),
        (501, "fënnefhonnertéischten"),
        (502, "fënnefhonnertzweeten"),
        (503, "fënnefhonnertdrëtten"),
        (504, "fënnefhonnertvéierten"),
        (505, "fënnefhonnertfënneften"),
        (506, "fënnefhonnertsechsten"),
        (507, "fënnefhonnertsiwenten"),
        (508, "fënnefhonnertaachten"),
        (509, "fënnefhonnertnéngten"),
        (510, "fënnefhonnertzéngten"),
        (511, "fënnefhonnerteeleften"),
        (600, "sechshonnertsten"),
        (601, "sechshonnertéischten"),
        (602, "sechshonnertzweeten"),
        (603, "sechshonnertdrëtten"),
        (604, "sechshonnertvéierten"),
        (605, "sechshonnertfënneften"),
        (606, "sechshonnertsechsten"),
        (607, "sechshonnertsiwenten"),
        (608, "sechshonnertaachten"),
        (609, "sechshonnertnéngten"),
        (610, "sechshonnertzéngten"),
        (611, "sechshonnerteeleften"),
        (700, "siwenhonnertsten"),
        (701, "siwenhonnertéischten"),
        (702, "siwenhonnertzweeten"),
        (703, "siwenhonnertdrëtten"),
        (704, "siwenhonnertvéierten"),
        (705, "siwenhonnertfënneften"),
        (706, "siwenhonnertsechsten"),
        (707, "siwenhonnertsiwenten"),
        (708, "siwenhonnertaachten"),
        (709, "siwenhonnertnéngten"),
        (710, "siwenhonnertzéngten"),
        (711, "siwenhonnerteeleften"),
        (800, "aachthonnertsten"),
        (801, "aachthonnertéischten"),
        (802, "aachthonnertzweeten"),
        (803, "aachthonnertdrëtten"),
        (804, "aachthonnertvéierten"),
        (805, "aachthonnertfënneften"),
        (806, "aachthonnertsechsten"),
        (807, "aachthonnertsiwenten"),
        (808, "aachthonnertaachten"),
        (809, "aachthonnertnéngten"),
        (810, "aachthonnertzéngten"),
        (811, "aachthonnerteeleften"),
        (900, "nénghonnertsten"),
        (901, "nénghonnertéischten"),
        (902, "nénghonnertzweeten"),
        (903, "nénghonnertdrëtten"),
        (904, "nénghonnertvéierten"),
        (905, "nénghonnertfënneften"),
        (906, "nénghonnertsechsten"),
        (907, "nénghonnertsiwenten"),
        (908, "nénghonnertaachten"),
        (909, "nénghonnertnéngten"),
        (910, "nénghonnertzéngten"),
        (911, "nénghonnerteeleften"),
        (1000, "eendausendsten"),
    ]
    for num, expected in cases:
        assert lb.to_ordinal(num) == expected, f"Ordinal {num}: {lb.to_ordinal(num)} != {expected}"


def test_currency():
    lb = Num2Word_LB()
    cases = [
        (1, 'EUR', "een Euro"),
        (2, 'EUR', "zwee Euro"),
        (1.01, 'EUR', "een Euro an een Cent"),
        (2.50, 'EUR', "zwee Euro an fofzeg Cent"),
        (0.01, 'EUR', "een Cent"),
        (1, 'USD', "een Dollar"),
        (2.25, 'USD', "zwee Dollar an fënnefanzwanzeg Cent"),
        (1, 'GBP', "een Pond"),
        (1, 'CNY', "een Yuan"),
        (1, 'DEM', "eng Mark"),
    ]
    for value, currency, expected in cases:
        result = lb.to_currency(value, currency=currency)
        assert expected in result, f"Currency {value} {currency}: {result} != {expected}"


def test_percentages():
    lb = Num2Word_LB()
    cases = [
        (25, "fënnefanzwanzeg Prozent"),
        (50, "fofzeg Prozent"),
        (75, "fënnefasiwwenzeg Prozent"),
        (1, "een Prozent"),
        (10, "zéng Prozent"),
        (99, "nénganzwanzeg Prozent"),
        (0.5, "null Komma fënnef Prozent"),
        (100, "honnert Prozent"),
    ]
    for value, expected in cases:
        result = lb.to_percentage(value)
        assert expected in result, f"Percentage {value}: {result} != {expected}"


def test_units():
    lb = Num2Word_LB()
    cases = [
        ("-1°", "minus een Grad"),
        ("-10°", "minus zéng Grad"),
        ("1kg", "ee Kilogramm"),
        ("2kg", "zwee Kilogramm"),
        ("1ml", "een Milliliter"),
        ("2ml", "zwee Milliliter"),
        ("1gr", "een Gramm"),
        ("2gr", "zwee Gramm"),
        ("10%", "zéng Prozent"),
        ("25%", "fënnefanzwanzeg Prozent"),
        ("50%", "fofzeg Prozent"),
        ("100%", "honnert Prozent"),
        ("1970er", "nonzénghonnertsiwenzeger"),
        ("2000er", "zwoudausender"),
    ]
    for text, expected in cases:
        result = lb.to_unit(text)
        assert expected in result, f"Unit '{text}': {result} != {expected}"


def test_years():
    lb = Num2Word_LB()
    cases = [
        (1970, "nonzénghonnertsiwenzeg"),
        (2000, "zwoudausend"),
        (2020, "zwoudausendzwanzeg"),
        (1985, "nonzénghonnertfënnefanzwanzeg"),
    ]
    for year, expected in cases:
        result = lb.to_year(year)
        assert expected in result, f"Year {year}: {result} != {expected}"


def test_large_numbers():
    lb = Num2Word_LB()
    cases = [
        (1000, "eendausend"),
        (1000000, "eng Millioun"),
        (1000000000, "eng Milliard"),
        (2000000, "zwee Milliounen"),
    ]
    for num, expected in cases:
        result = lb.to_cardinal(num)
        assert expected in result, f"Large number {num}: {result} != {expected}"


def test_edge_cases():
    lb = Num2Word_LB()
    cases = [
        (0, "null"),
        (-1, "minus een"),
        (1.5, "een Komma fënnef"),
        (-10, "minus zéng"),
        (0.01, "null Komma een"),
    ]
    for num, expected in cases:
        result = lb.to_cardinal(num)
        assert expected in result, f"Edge case {num}: {result} != {expected}"


def main():
    """Run all tests"""
    test_normalizer()
    print("Tests completed.")


if __name__ == "__main__":
    main()
    print("\n=== RUNNING EXTENDED TESTS ===\n")
    test_ordinals()
    print("Ordinals: OK")
    test_currency()
    print("Currency: OK")
    test_percentages()
    print("Percentages: OK")
    test_units()
    print("Units: OK")
    test_years()
    print("Years: OK")
    test_large_numbers()
    print("Large numbers: OK")
    test_edge_cases()
    print("Edge cases: OK")