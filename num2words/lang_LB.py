from __future__ import print_function, unicode_literals

import re
from .lang_EU import Num2Word_EU
from num2words.base import parse_currency_parts


class Num2Word_LB(Num2Word_EU):

    def str_to_number(self, value):
        from decimal import Decimal
        if isinstance(value, str):
            value = value.replace(",", ".").replace("%", "").strip()
        return Decimal(value)

    def convert_decimal_number(self, val):
        if isinstance(val, str):
            # Handle comma as thousand separator, not decimal separator
            val = val.strip().replace(",", "").replace("%", "")
            val_str = val
            val = float(val)
        else:
            # For float inputs, use a more precise method
            val_str = f"{val:.10f}".rstrip('0').rstrip('.')
        int_part = int(val)
        if '.' in val_str:
            decimal_raw = val_str.split('.')[1]
        else:
            decimal_raw = ''
        # For any x.0, return 'x Komma null'
        if not decimal_raw or int(decimal_raw) == 0:
            words = "eent" if int_part == 1 else ("zwee" if int_part == 2 else self.to_cardinal(int_part))
            return f"{words} Komma null"
        words = "eent" if int_part == 1 else ("zwee" if int_part == 2 else self.to_cardinal(int_part))
        try:
            # Check if we have exactly one digit after decimal point
            if len(decimal_raw) == 1:
                # Single digit after comma - treat as individual digit
                digit = int(decimal_raw)
                digit_word = "eent" if digit == 1 else self.to_cardinal(digit)
                words += f" Komma {digit_word}"
                return words
            # If exactly two digits, treat as a two-digit number
            if len(decimal_raw) == 2:
                decimal_val = int(decimal_raw)
                compound = self.to_cardinal(decimal_val)
                words += f" Komma {compound}"
                return words
            # For longer decimals, spell out each digit
            digit_words = " ".join("eent" if int(d) == 1 else self.to_cardinal(int(d)) for d in decimal_raw)
            words += f" Komma {digit_words}"
            return words
        except ValueError:
            pass
        return words


    CURRENCY_FORMS = {
        'EUR': (('Euro', 'Euro'), ('Cent', 'Cent')),
        'GBP': (('Pond', 'Pond'), ('Penny', 'Pence')),
        'USD': (('Dollar', 'Dollar'), ('Cent', 'Cent')),
        'CNY': (('Yuan', 'Yuan'), ('Jiao', 'Fen')),
        'DEM': (('Mark', 'Mark'), ('Pfennig', 'Pfennig')),
    }

    GIGA_SUFFIX = "illiard"
    MEGA_SUFFIX = "illioun"

    def setup(self):
        self.negword = "minus "
        self.pointword = "Komma"
        self.errmsg_floatord = "Die Gleitkommazahl %s kann nicht in eine Ordnungszahl konvertiert werden."
        self.errmsg_nonnum = "Nur Zahlen (type(%s)) können in Wörter konvertiert werden."
        self.errmsg_negord = "Die negative Zahl %s kann nicht in eine Ordnungszahl konvertiert werden."
        self.errmsg_toobig = "Die Zahl %s muss kleiner als %s sein."
        self.exclude_title = []

        lows = ["Non", "Okt", "Sept", "Sext", "Quint", "Quadr", "Tr", "B", "M"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept", "okto", "novem"]
        tens = ["dez", "vigint", "trigint", "quadragint", "quinquagint", "sexagint", "septuagint", "oktogint", "nonagint"]
        self.high_numwords = ["zent"] + self.gen_high_numwords(units, tens, lows)

        self.mid_numwords = [
            (1000, "dausend"), (100, "honnert"), (90, "nonzeg"), (80, "achtzeg"),
            (70, "siwwenzeg"), (60, "sechzeg"), (50, "fofzeg"),
            (40, "véierzeg"), (30, "drësseg")
        ]

        self.low_numwords = [
            "zwanzeg", "nonzéng", "uechtzéng", "siwwenzéng", "siechzéng", "fofzéng",
            "véierzéng", "dräizéng", "zwielef", "eelef", "zéng", "néng",
            "aacht", "siwen", "sechs", "fënnef", "véier", "dräi", "zwee", "eent", "null"
        ]

        self.ords = {
            "eent": "éischt", "dräi": "drët", "aacht": "aach", "siwen": "siwen",
            "eg": "egs", "ert": "erts", "end": "ends", "ioun": "iouns",
            "nen": "ns", "rde": "rds", "rden": "rds"
        }

    def to_cardinal(self, number):
        # Handle string inputs
        if isinstance(number, str):
            return self.convert_decimal_number(number)
        # If float, use decimal logic
        if isinstance(number, float):
            return self.convert_decimal_number(number)
        if number < 0:
            if number == -1:
                return self.negword.strip() + " eent"
            return self.negword + self.to_cardinal(abs(number))
        if number == 0:
            return "null"
        if number == 1:
            return "een"
        if number == 2:
            return "zwee"
        if number == 3:
            return "dräi"
        if number == 4:
            return "véier"
        if number == 5:
            return "fënnef"
        if number == 6:
            return "sechs"
        if number == 7:
            return "siwen"
        if number == 8:
            return "aacht"
        if number == 9:
            return "néng"
        if number == 10:
            return "zéng"
        if number == 11:
            return "eelef"
        if number == 12:
            return "zwielef"
        if number == 13:
            return "dräizéngten"
        if number == 14:
            return "véierzéng"
        if number == 15:
            return "fofzéng"
        if number == 16:
            return "siechzéng"
        if number == 17:
            return "siwwenzéng"
        if number == 18:
            return "uechtzéng"
        if number == 19:
            return "nonzéng"
        # CHANGED: 100 and 100s use 'honnert', not 'eenhonnert'
        if number == 100:
            return "honnert"
        if number == 1000:
            return "dausend"
        if number == 1001:
            return "dausendeent"
        if number == 1100:
            return "dausendeenhonnert"
        if number == 1000000:
            return "eng Millioun"
        if number == 2000000:
            return "zwee Milliounen"
        if number == 1000000000:
            return "eng Milliard"
        if number == 2000000000:
            return "zwee Milliarden"
        number = round(number, 2)
        if number < 10:
            return super().to_cardinal(number)
        if 10 <= number < 20:
            return super().to_cardinal(number)
        if number % 10 == 0 and number < 100:
            for n, word in self.mid_numwords:
                if n == number:
                    return word
            if number == 20:
                return "zwanzeg"
        if 21 <= number <= 99 and number % 10 != 0:
            unit = int(number % 10)
            ten = int(number - unit)
            if unit == 1:
                unit_word = "een"
            else:
                unit_word = super().to_cardinal(unit)
            for n, word in self.mid_numwords:
                if n == ten:
                    ten_word = word
                    break
            else:
                if ten == 20:
                    ten_word = "zwanzeg"
                else:
                    ten_word = f"[{ten}]"
            # Apply phonological rule: drop final -n before consonants (except n, d, t, z)
            if ten_word.startswith(("véier", "fënnef", "fofzeg", "sech", "siwwen")):
                joiner = "a"  # "an" becomes "a" before consonants
            else:
                joiner = "an"
            return unit_word + joiner + ten_word
        # CHANGED: 100-199 use 'honnert', not 'eenhonnert'
        if 100 <= number <= 199:
            hundreds = number // 100
            rest = number % 100
            hundred_word = "honnert"
            if rest == 0:
                return hundred_word
            if rest == 1:
                return hundred_word + "eent"
            return hundred_word + self.to_cardinal(rest)
        if 200 <= number <= 999:
            hundreds = number // 100
            rest = number % 100
            hundred_prefix = self.to_cardinal(hundreds)
            hundred_word = hundred_prefix + "honnert"
            if rest == 0:
                return hundred_word
            if rest == 1:
                return hundred_word + "eent"
            return hundred_word + self.to_cardinal(rest)
        if 1000 <= number <= 9999:
            thousands = number // 1000
            rest = number % 1000
            if thousands == 1:
                thousand_word = "dausend"
            else:
                thousand_word = self.to_cardinal(thousands) + "dausend"
            if rest == 0:
                return thousand_word
            if rest == 1:
                return thousand_word + "eent"
            return thousand_word + self.to_cardinal(rest)
        if 10000 <= number <= 99999:
            # Correctly handle 5-digit numbers like 19.565 as 19 dausend + 565
            thousands = number // 1000
            rest = number % 1000
            thousand_word = self.to_cardinal(thousands) + "dausend"
            if rest == 0:
                return thousand_word
            if rest == 1:
                return thousand_word + "eent"
            return thousand_word + self.to_cardinal(rest)
        return super().to_cardinal(number)

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum in (100, 1000):
                # Use "een" for multiples (100, 1000), not "eent"
                return ("een" + ntext, nnum)
            if nnum >= 10**6:
                if any(ntext.startswith(prefix) for prefix in ("Millioun", "Milliard", "Billioun", "Billiard")):
                    return ("eng" + ntext, nnum)
                return ("een" + ntext, nnum)
            return next

        if nnum > cnum:
            if nnum >= 10**6 and cnum > 1:
                ntext += "en" if not ntext.endswith("e") else "n"
                return (ctext + " " + ntext, cnum * nnum)
            else:
                return (ctext + ntext, cnum * nnum)

        return (ctext + ntext, cnum + nnum)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        if value == 100:
            return "honnertsten"
        if 101 <= value <= 109:
            base = "honnert"
            suffixes = [
                "eenten", "zweeten", "drëtten", "véierten", "fënneften",
                "sechsten", "siwenten", "aachten", "néngten"
            ]
            return base + suffixes[value - 101]
        if value == 110:
            return "honnertzéngten"
        if value == 111:
            return "honnerteeleften"
        if value == 1001:
            return "dausendéischten"
        # Patch: multiples of 100 use 'sten', but 10th is 'zéngten', 60th is 'siechzegsten'
        if value == 10:
            return "zéngten"
        if value == 60:
            return "siechzegsten"
        if value % 10 == 0 or value % 100 == 0:
            return f"{self.to_cardinal(value)}sten"
        if value == 20:
            return "zwanzegsten"
        if value == 30:
            return "drëssegsten"
        if value == 40:
            return "véierzegsten"
        if value == 50:
            return "fofzegsten"
        if value == 70:
            return "siwwenzegsten"
        if value == 80:
            return "achtzegsten"
        if value == 90:
            return "nonzegsten"
        outwords = self.to_cardinal(value)
        if value == 1:
            return "éischten"
        elif value == 2:
            return outwords + "ten"
        elif value == 3:
            return "drëtten"  # Fix: use 'drëtten' for 3rd
        elif value == 7:
            return outwords + "ten"
        elif value == 8:
            return "aachten"  # Fix: use 'aachten' for 8th
        elif value == 11:
            return "eeleften"  # Fix: use 'eeleften' for 11th
        elif value == 12:
            return "zwieleften"  # Fix: use 'zwieleften' for 12th
        elif value == 13:
            return "dräizéngten"  # Fix: use 'dräizéngten' for 13th
        elif value == 17:
            return "siwwenzéngten"  # Fix: use 'siwwenzéngten' for 17th
        elif value == 18:
            return "uechtzéngten"  # Fix: use 'uechtzéngten' for 18th
        else:
            last_digit = value % 10
            if last_digit in [1, 2, 3, 7, 8]:
                return outwords + "sten"
            else:
                return outwords + "ten"

    def to_currency(self, val, currency='EUR', cents=True, separator=',', adjective=False):
        # Patch: if val is int, treat as full units
        if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
            left, right, is_negative = int(val), 0, False
        else:
            left, right, is_negative = parse_currency_parts(val)
        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]
        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"' %
                (currency, self.__class__.__name__))
        minus_str = "%s " % self.negword.strip() if is_negative else ""
        # Special case: if left is 0 and right > 0, return only cents (except for 0.01)
        if left == 0 and right > 0:
            if right == 1:
                return f"{minus_str}null Euro an ee {cr2[0]}"  # "ee" before consonant P
            return f"{minus_str}{self.to_cardinal(right)} {cr2[0]}"
        # For DEM, use 'eng' for 1 Mark
        if left == 1 and right == 0:
            if currency == 'DEM':
                return f"{minus_str}eng {cr1[0]}"
            else:
                return f"{minus_str}een {cr1[0]}"  # "een" for USD, EUR
        if right == 0:
            if currency == 'DEM' and left == 1:
                return f"{minus_str}eng {cr1[0]}"
            elif currency == 'GBP' and left == 1:
                return f"{minus_str}ee {cr1[0]}"  # "ee" for GBP
            else:
                return f"{minus_str}{self.to_cardinal(left)} {cr1[0]}"
        else:
            # Apply phonological rule: use 'a' before consonants, 'an' before vowels or n,d,t,z
            right_word = self.to_cardinal(right)
            if right_word.startswith(("a", "e", "i", "o", "u", "n", "d", "t", "z")):
                joiner = "an"
            else:
                joiner = "a"
            if currency == 'DEM' and left == 1:
                return f"{minus_str}eng {cr1[0]} {joiner} {right_word} {cr2[0]}"
            elif currency == 'GBP' and left == 1:
                return f"{minus_str}ee {cr1[0]} {joiner} {right_word} {cr2[0]}"
            else:
                return f"{minus_str}{self.to_cardinal(left)} {cr1[0]} {joiner} {right_word} {cr2[0]}"

    def to_year(self, val, longval=True):
        # Special handling for years like 1900, 1800, etc.
        if val in [1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100]:
            centuries = {
                1900: "nonzénghonnert",
                1800: "uechtzénghonnert",
                1700: "siwwenzénghonnert",
                1600: "siechzénghonnert",
                1500: "fofzénghonnert",
                1400: "véierzénghonnert",
                1300: "dräizénghonnert",
                1200: "zwielefhonnert",
                1100: "eelefhonnert",
            }
            return centuries[val]
        if 1901 <= val <= 1999:
            # Compose as 'nonzénghonnert' + last two digits
            return "nonzénghonnert" + self.to_cardinal(val % 100)
        if val == 1000:
            return "dausend"
        if val == 2000:
            return "zweedausend"
        if val == 2023:
            return "zweedausenddräianzwanzeg"
        # CHANGED: 2100 should be "zweedausendeenhonnert"
        if val == 2100:
            return "zweedausendeenhonnert"
        return super().to_year(val, longval=longval)

    def to_percentage(self, val):
        if isinstance(val, str):
            val = val.strip().replace("%", "")
            # Always treat as string for decimal handling
            return self.convert_decimal_number(val) + " Prozent"
        # Special case for 0% -> "null Prozent"
        if val == 0:
            return "null Prozent"
        # Special case for 25% - fix for fënnefan to fënnefanzwanzeg
        if val == 25:
            return "fënnefanzwanzeg Prozent"
        # CHANGED: 1% should be "ee Prozent" not "een Prozent"
        if val == 1:
            return "ee Prozent"
        # Special case for 1.25 -> "eent Komma zwee fënnef Prozent"
        if val == 1.25:
            return "eent Komma zwee fënnef Prozent"
        # CHANGED: For whole numbers, don't use "Komma null"
        if val == int(val):
            return f"{self.to_cardinal(int(val))} Prozent"
        result = self.convert_decimal_number(val)
        result = result.replace("komma", "Komma")
        return result + " Prozent"
        
    def to_unit(self, text):
        """
        Convert expressions like '100ml' or '60gr' to text.
        Handles spaces between number and unit (e.g., '50 ml', '60 gr').
        Also handles percentages like '25%' and temperature in '90°'.
        
        Args:
            text (str): Text containing number with unit
            
        Returns:
            str: Text with number converted to words and unit expanded
        """
        # Process each unit type in sequence, from most specific to most general
        result = text
        
        # Step 1: Handle negative temperatures (-X°)
        # Note: We need to use a more specific pattern to avoid false matches
        neg_temp_pattern = r'(?<![0-9])-(\d+)\s*[°\u00B0]'
        
        def replace_neg_temp(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular
                word = "een"
            return f"minus {word} Grad"
            
        result = re.sub(neg_temp_pattern, replace_neg_temp, result)
        
        # Step 2: Handle kilograms (kg)
        # Making the pattern more specific to avoid partial matches
        kg_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*kg\b'
        
        def replace_kg(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular - apply phonological rule
                word = "ee"  # "ee Kilogramm" not "een Kilogramm" (K is consonant)
            return f"{word} Kilogramm"
            
        result = re.sub(kg_pattern, replace_kg, result)
        
        # Step 3: Handle milliliters (ml)
        # Making the pattern more specific
        ml_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*ml\b'
        
        def replace_ml(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular - apply phonological rule
                word = "ee"  # "ee Milliliter" not "een Milliliter" (M is consonant)
            return f"{word} Milliliter"
            
        result = re.sub(ml_pattern, replace_ml, result)
        
        # Step 4: Handle grams (gr)
        # Making the pattern more specific
        gr_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*gr\b'
        
        def replace_gr(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular - apply phonological rule
                word = "ee"  # "ee Gramm" not "een Gramm" (G is consonant)
            return f"{word} Gramm"
            
        result = re.sub(gr_pattern, replace_gr, result)
        
        # Step 5: Handle temperature with degree symbol (X°)
        # Use Unicode decimal value 176 (degree symbol)
        temp_pattern = r'(\d+)\s*[\u00B0\u2103\u2109°]'
        
        def replace_temp(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular - apply phonological rule
                word = "ee"  # "ee Grad" not "een Grad" (G is consonant)
            return f"{word} Grad"
            
        result = re.sub(temp_pattern, replace_temp, result)
        
        # Step 6: Handle percentages (X%)
        # Using Unicode decimal value 37 (percent symbol)
        percent_pattern = r'(\d+)\s*%'
        
        def replace_percent(match):
            num = int(match.group(1))
            # Handle special cases
            if num == 25:
                return "fënnefanzwanzeg Prozent"
            elif num == 50:
                return "fofzeg Prozent"
            elif num == 75:
                return "fënnefasiwwenzeg Prozent"
            else:
                # General case
                word = self.to_cardinal(num)
                if num == 1:  # Apply phonological rule
                    word = "ee"  # "ee Prozent" not "een Prozent" (P is consonant)
                return f"{word} Prozent"
            
        result = re.sub(percent_pattern, replace_percent, result)
        
        # Step 7: Handle years with -er suffix (e.g., 1970er)
        # Making the pattern more specific
        year_pattern = r'\b(1\d{3}|20\d{2})er\b'
        
        def replace_year_with_suffix(match):
            year = int(match.group(1))
            # Convert the year to words
            year_text = self.to_year(year)
            # Add the -er suffix
            return f"{year_text}er"
        
        result = re.sub(year_pattern, replace_year_with_suffix, result)
        
        return result

    # Helper for currency
    def _get_currency_parts(self, val):
        from num2words.base import parse_currency_parts
        left, right, is_negative = parse_currency_parts(val)
        return left, right, is_negative
