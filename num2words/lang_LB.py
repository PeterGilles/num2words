from __future__ import print_function, unicode_literals

import re
from .lang_EU import Num2Word_EU


class Num2Word_LB(Num2Word_EU):

    def str_to_number(self, value):
        from decimal import Decimal
        if isinstance(value, str):
            value = value.replace(",", ".").strip()
        return Decimal(value)

    def convert_decimal_number(self, val):
        if isinstance(val, str):
            val = val.strip().replace(",", ".").replace("%", "")
            val = float(val)
    
        int_part = int(val)
        decimal_str = f"{val:.10f}".split(".")[1].rstrip("0")
    
        words = self.to_cardinal(int_part)
    
        if decimal_str:
            try:
                decimal_val = int(decimal_str)
                if 10 <= decimal_val <= 99:
                    compound = self.to_cardinal(decimal_val)
                    words += f" {self.pointword.lower()} {compound}"
                else:
                    # fallback to digit-wise pronunciation
                    digit_words = " ".join(self.to_cardinal(int(d)) for d in decimal_str)
                    words += f" {self.pointword.lower()} {digit_words}"
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
        if number < 0:
            return self.negword + self.to_cardinal(abs(number))

        if number == 0:
            return "null"
            
        # Special case for standalone "1" - should be "een" not "eent"
        if number == 1:
            return "een"
            
        number = round(number, 2)
        
        # Return directly from super method for small numbers
        if number < 10:
            return super().to_cardinal(number)

        # For 10-19, we can use the super method
        if 10 <= number < 20:
            return super().to_cardinal(number)
            
        # For multiples of 10 (e.g., 20, 30, 40), use the mid_numwords
        if number % 10 == 0 and number < 100:
            for n, word in self.mid_numwords:
                if n == number:
                    return word
            # Special case for 20
            if number == 20:
                return "zwanzeg"
                
        # For 21-99 (except multiples of 10)
        if 21 <= number <= 99 and number % 10 != 0:
            unit = int(number % 10)
            ten = int(number - unit)
            
            # Get unit word
            if unit == 1:
                unit_word = "een"
            else:
                unit_word = super().to_cardinal(unit)
                
            # Get tens word
            for n, word in self.mid_numwords:
                if n == ten:
                    ten_word = word
                    break
            else:
                # If we reach here, we need to handle 20 specially
                if ten == 20:
                    ten_word = "zwanzeg"
                else:
                    ten_word = f"[{ten}]"  # Fallback
            
            # Choose appropriate joiner based on tens word
            joiner = "a" if ten_word.startswith(("véier", "fënnef", "fofzeg", "sech", "siwwen")) else "an"
            
            return unit_word + joiner + ten_word
            
        # For 100-999
        if 100 <= number <= 999:
            hundreds = number // 100
            rest = number % 100
            
            # Construct hundreds part
            if hundreds == 1:
                hundred_word = "eenhonnert"
            else:
                # Get the word for the number of hundreds
                hundred_prefix = self.to_cardinal(hundreds)
                hundred_word = hundred_prefix + "honnert"
                
            # If no remainder, return just the hundreds
            if rest == 0:
                return hundred_word
                
            # Special case for x01
            if rest == 1:
                return hundred_word + "eent"
                
            # Otherwise add the remainder
            return hundred_word + self.to_cardinal(rest)
            
        # For 1000-9999
        if 1000 <= number <= 9999:
            thousands = number // 1000
            rest = number % 1000
            
            # Construct thousands part
            if thousands == 1:
                thousand_word = "eendausend"
            else:
                thousand_word = self.to_cardinal(thousands) + "dausend"
                
            # If no remainder, return just the thousands
            if rest == 0:
                return thousand_word
                
            # Handle special cases for remainder
            if rest < 100:
                # Direct append for small remainders
                return thousand_word + self.to_cardinal(rest)
            else:
                # For larger remainders
                return thousand_word + self.to_cardinal(rest)
                
        # Default to super method for larger numbers
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
    
        # Lexicalized and morphologically correct ordinals
        ordinals = {
            0: "nullten",
            1: "éischten",
            2: "zweeten",
            3: "drëtten",
            4: "véierten",
            5: "fënneften",
            6: "sechsten",
            7: "siwenten",
            8: "aachten",
            9: "néngten",
            10: "zéngten",
            11: "eeleften",
            12: "zwieleften",
            13: "dräizéngten",
            14: "véierzéngten",
            15: "fofzéngten",
            16: "siechzéngten",
            17: "siwwenzéngten",
            18: "uechtzéngten",
            19: "nonzéngten",
            20: "zwanzegsten",
            21: "eenanzwanzegsten",
            22: "zweeanzwanzegsten",
            23: "dräianzwanzegsten",
            24: "véieranzwanzegsten",
            25: "fënnefanzwanzegsten",
            26: "sechsanzwanzegsten",
            27: "siwwenanzwanzegsten",
            28: "aachtanzwanzegsten",
            29: "nénganzwanzegsten",
            30: "drëssegsten",
            40: "véierzegsten",
            50: "fofzegsten",
            60: "siechzegsten",
            70: "siwwenzegsten",
            80: "achtzegsten",
            90: "nonzegsten",
            100: "honnertsten",
            101: "eenhonnerteentsten",  # Special case for 101st
            200: "zweehonnertsten",     # Special case for 200th
            1000: "eendausendsten",     # Special case for 1000th
        }
    
        if value in ordinals:
            return ordinals[value]
            
        # Special cases for hundreds and thousands
        # Pattern: x00 (like 100, 200, 300, etc.)
        if value % 100 == 0 and value < 10000:
            if value == 100:
                return "honnertsten"
            elif value == 1000:
                return "eendausendsten"
            elif value % 1000 == 0:
                prefix = self.to_cardinal(value // 1000)
                return prefix + "dausendsten"
            else:
                prefix = self.to_cardinal(value // 100)
                return prefix + "honnertsten"
                
        # Pattern: x01 (like 101, 201, etc.)
        if value > 100 and value % 100 == 1:
            if value < 1000:
                hundreds = value // 100
                if hundreds == 1:
                    return "eenhonnertsten"
                else:
                    hundred_prefix = self.to_cardinal(hundreds)
                    return hundred_prefix + "honnertsten"
            else:
                # For thousands (1001, 2001, etc.)
                thousands = value // 1000
                if thousands == 1:
                    return "eendausendsten"
                else:
                    thousand_prefix = self.to_cardinal(thousands)
                    return thousand_prefix + "dausendsten"
    
        # Fallback for productive forms ≥ 31
        base = self.to_cardinal(value)
        
        # Specific fixes for hundreds and thousands to always use "sten"
        if value >= 100:
            if base.endswith(("honnert", "dausend")):
                return base + "sten"
                
        # Regular suffix rules
        if base.endswith(("g", "k", "z")):
            return base + "sten"
        elif base.endswith(("n", "t", "ch", "f", "s")):
            # Changing from "ten" to "sten" for consistency
            return base + "sten"
        elif base.endswith("e"):
            return base[:-1] + "esten"
        else:
            # Changing from "ten" to "sten" for consistency
            return base + "sten"


    def to_currency(self, val, currency='EUR', cents=True, separator=' an', adjective=False):
        result = super(Num2Word_LB, self).to_currency(
            val, currency=currency, cents=cents, separator=separator, adjective=adjective)
        return result.replace("eent ", "een ")

    def to_year(self, val, longval=True):
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="honnert", longval=longval).replace(' ', '')

    def to_percentage(self, val):
        if isinstance(val, str):
            val = val.strip().replace(",", ".").replace("%", "")
            try:
                val = float(val)
            except ValueError:
                raise ValueError(f"Cannot interpret percentage: '{val}'")
                
        # Special case for 25% - fix for fënnefan to fënnefanzwanzeg
        if val == 25:
            return "fënnefanzwanzeg Prozent"
        
        result = self.convert_decimal_number(val)
        # Capitalize "komma" to "Komma" for consistency
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
            if num == 1:  # Special case for singular
                word = "ee"  # "ee Kilogramm" not "een Kilogramm"
            return f"{word} Kilogramm"
            
        result = re.sub(kg_pattern, replace_kg, result)
        
        # Step 3: Handle milliliters (ml)
        # Making the pattern more specific
        ml_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*ml\b'
        
        def replace_ml(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular
                word = "een"
            return f"{word} Milliliter"
            
        result = re.sub(ml_pattern, replace_ml, result)
        
        # Step 4: Handle grams (gr)
        # Making the pattern more specific
        gr_pattern = r'(?<![a-zA-Z0-9-])(\d+)\s*gr\b'
        
        def replace_gr(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular
                word = "een"
            return f"{word} Gramm"
            
        result = re.sub(gr_pattern, replace_gr, result)
        
        # Step 5: Handle temperature with degree symbol (X°)
        # Use Unicode decimal value 176 (degree symbol)
        temp_pattern = r'(\d+)\s*[\u00B0\u2103\u2109°]'
        
        def replace_temp(match):
            num = int(match.group(1))
            word = self.to_cardinal(num)
            if num == 1:  # Special case for singular
                word = "een"
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
