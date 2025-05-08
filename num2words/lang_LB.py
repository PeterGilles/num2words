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
            (1000, "dausend"), (100, "honnert"), (90, "nonnzeg"), (80, "achtzeg"),
            (70, "siwenzeg"), (60, "sechzeg"), (50, "foffzeg"),
            (40, "véierzeg"), (30, "drësseg")
        ]

        self.low_numwords = [
            "zwanzeg", "nonnzéng", "uechtzéng", "siwenzéng", "siechzéng", "foffzéng",
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

        number = round(number, 2)

        units_map = {
            0: "null", 1: "een", 2: "zwee", 3: "dräi", 4: "véier", 5: "fënnef",
            6: "sechs", 7: "siwen", 8: "aacht", 9: "néng"
        }
        tens_map = dict(self.mid_numwords)

        if 100 <= number <= 999:
            hundreds = number // 100
            rest = int(number % 100)
            hundred_word = self.to_cardinal(hundreds) + "honnert"
            if rest == 0:
                return hundred_word
            elif 21 <= rest <= 99 and rest % 10 != 0:
                unit = rest % 10
                ten = rest - unit
                unit_word = units_map[unit]
                ten_word = tens_map.get(ten, "")
                joiner = "a" if ten_word.startswith(("véier", "fënnef", "foffzeg", "sech", "siwen")) else "an"
                return hundred_word + unit_word + joiner + ten_word
            else:
                return hundred_word + self.to_cardinal(rest)

        if 21 <= number <= 99 and number % 10 != 0:
            unit = int(number % 10)
            ten = int(number - unit)
            unit_word = units_map[unit]
            ten_word = tens_map.get(ten, "")
            joiner = "a" if ten_word.startswith(("véier", "fënnef", "foffzeg", "sech", "siwen")) else "an"
            return unit_word + joiner + ten_word

        return super().to_cardinal(number)

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum in (100, 1000):
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
            11: "eelften",
            12: "zwieleften",
            13: "dräizéngten",
            14: "véierzéngten",
            15: "fofzéngten",
            16: "siechzéngten",
            17: "siwwenzéngten",
            18: "uechtzéngten",
            19: "nonnzéngten",
            20: "zwanzegsten",
            21: "eenanzwanzegsten",
            22: "zweeanzwanzegsten",
            23: "dräianzwanzegsten",
            24: "véieranzwanzegsten",
            25: "fënnefanzwanzegsten",
            26: "sechsanzwanzegsten",
            27: "siwenanzwanzegsten",
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
        }
    
        if value in ordinals:
            return ordinals[value]
    
        # Fallback for productive forms ≥ 31
        base = self.to_cardinal(value)
        if base.endswith(("g", "k", "z")):
            return base + "sten"
        elif base.endswith(("n", "t", "ch", "f", "s")):
            return base + "ten"
        elif base.endswith("e"):
            return base[:-1] + "esten"
        else:
            return base + "ten"


    def to_currency(self, val, currency='EUR', cents=True, separator=' an', adjective=False):
        result = super(Num2Word_DE, self).to_currency(
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
        return self.convert_decimal_number(val) + " Prozent"
