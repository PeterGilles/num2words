#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from num2words import num2words
from num2words.lang_LB import Num2Word_LB


class Num2WordsLBTests(unittest.TestCase):
    def setUp(self):
        self.n2w = Num2Word_LB()

    def test_cardinal(self):
        test_cases = [
            (0, "null"),
            (1, "een"),
            (2, "zwee"),
            (3, "dräi"),
            (4, "véier"),
            (5, "fënnef"),
            (6, "sechs"),
            (7, "siwen"),
            (8, "aacht"),
            (9, "néng"),
            (10, "zéng"),
            (11, "eelef"),
            (12, "zwielef"),
            (13, "dräizéng"),
            (14, "véierzéng"),
            (15, "fofzéng"),
            (16, "siechzéng"),
            (17, "siwwenzéng"),
            (18, "uechtzéng"),
            (19, "nonzéng"),
            (20, "zwanzeg"),
            (21, "eenanzwanzeg"),
            (22, "zweeanzwanzeg"),
            (23, "dräianzwanzeg"),
            (24, "véieranzwanzeg"),
            (25, "fënnefanzwanzeg"),
            (26, "sechsanzwanzeg"),
            (27, "siwenanzwanzeg"),
            (28, "aachtanzwanzeg"),
            (29, "nénganzwanzeg"),
            (30, "drësseg"),
            (31, "eenandrësseg"),
            (40, "véierzeg"),
            (41, "eenavéierzeg"),
            (42, "zweeavéierzeg"),
            (50, "fofzeg"),
            (51, "eenafofzeg"),
            (52, "zweeafofzeg"),
            (53, "dräiafofzeg"),
            (60, "sechzeg"),
            (61, "eenasechzeg"),
            (64, "véierasechzeg"),
            (70, "siwwenzeg"),
            (71, "eenasiwwenzeg"),
            (75, "fënnefasiwwenzeg"),
            (80, "achtzeg"),
            (81, "eenanachtzeg"),
            (90, "nonzeg"),
            (91, "eenannonzeg"),
            (99, "néngannonzeg"),
            (100, "honnert"),
            (101, "honnerteent"),
            (102, "honnertzwee"),
            (110, "honnertzéng"),
            (111, "honnerteelef"),
            (200, "zweehonnert"),
            (201, "zweehonnerteent"),
            (999, "nénghonnertnéngannonzeg"),
            (1000, "dausend"),
            (1001, "dausendeent"),
            (1002, "dausendzwee"),
            (1010, "dausendzéng"),
            (1100, "dausendeenhonnert"),
            (2000, "zweedausend"),
            (2001, "zweedausendeent"),
            (9999, "néngdausendnénghonnertnéngannonzeg"),
            (1000000, "eng Millioun"),
            (2000000, "zwee Milliounen"),
            (1000000000, "eng Milliard"),
            (2000000000, "zwee Milliarden"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb'), word)

    def test_ordinal(self):
        test_cases = [
            (1, "éischten"),
            (2, "zweeten"),
            (3, "drëtten"),
            (4, "véierten"),
            (5, "fënneften"),
            (6, "sechsten"),
            (7, "siwenten"),
            (8, "aachten"),
            (9, "néngten"),
            (10, "zéngten"),
            (11, "eeleften"),
            (12, "zwieleften"),
            (13, "dräizéngten"),
            (14, "véierzéngten"),
            (15, "fofzéngten"),
            (16, "siechzéngten"),
            (17, "siwwenzéngten"),
            (18, "uechtzéngten"),
            (19, "nonzéngten"),
            (20, "zwanzegsten"),
            (21, "eenanzwanzegsten"),
            (22, "zweeanzwanzegsten"),
            (30, "drëssegsten"),
            (31, "eenandrëssegsten"),
            (40, "véierzegsten"),
            (50, "fofzegsten"),
            (60, "siechzegsten"),
            (70, "siwwenzegsten"),
            (80, "achtzegsten"),
            (90, "nonzegsten"),
            (100, "honnertsten"),
            (101, "honnerteenten"),
            (102, "honnertzweeten"),
            (110, "honnertzéngten"),
            (200, "zweehonnertsten"),
            (1000, "dausendsten"),
            (1001, "dausendéischten"),
            (2000, "zweedausendsten"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='ordinal'), word)

    def test_currency_eur(self):
        test_cases = [
            (0.01, "null Euro an een Cent"),
            (0.10, "zéng Cent"),
            (0.25, "fënnefanzwanzeg Cent"),
            (0.50, "fofzeg Cent"),
            (0.99, "néngannonzeg Cent"),
            (1.00, "een Euro"),
            (1.01, "een Euro an een Cent"),
            (1.10, "een Euro an zéng Cent"),
            (1.21, "een Euro an eenanzwanzeg Cent"),
            (1.25, "een Euro a fënnefanzwanzeg Cent"),
            (1.50, "een Euro a fofzeg Cent"),
            (1.53, "een Euro an dräiafofzeg Cent"),
            (1.99, "een Euro an néngannonzeg Cent"),
            (2.00, "zwee Euro"),
            (2.01, "zwee Euro an een Cent"),
            (2.10, "zwee Euro an zéng Cent"),
            (2.21, "zwee Euro an eenanzwanzeg Cent"),
            (2.24, "zwee Euro a véieranzwanzeg Cent"),
            (2.25, "zwee Euro a fënnefanzwanzeg Cent"),
            (2.26, "zwee Euro a sechsanzwanzeg Cent"),
            (2.27, "zwee Euro a siwenanzwanzeg Cent"),
            (2.47, "zwee Euro a siwenavéierzeg Cent"),
            (2.50, "zwee Euro a fofzeg Cent"),
            (2.99, "zwee Euro an néngannonzeg Cent"),
            (10.00, "zéng Euro"),
            (100.00, "honnert Euro"),
            (1000.00, "dausend Euro"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='currency'), word)

    def test_currency_usd(self):
        test_cases = [
            (1.00, "een Dollar"),
            (2.00, "zwee Dollar"),
            (1.01, "een Dollar an een Cent"),
            (1.25, "een Dollar an fënnefanzwanzeg Cent"),
            (2.25, "zwee Dollar an fënnefanzwanzeg Cent"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='currency', currency='USD'), word)

    def test_currency_gbp(self):
        test_cases = [
            (1.00, "ee Pond"),
            (2.00, "zwee Pond"),
            (1.01, "ee Pond an ee Penny"),
            (1.25, "ee Pond an fënnefanzwanzeg Penny"),
            (2.25, "zwee Pond a fënnefanzwanzeg Penny"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='currency', currency='GBP'), word)

    def test_currency_dem(self):
        test_cases = [
            (1.00, "eng Mark"),
            (2.00, "zwee Mark"),
            (1.01, "eng Mark an ee Pfennig"),
            (1.25, "eng Mark a fënnefanzwanzeg Pfennig"),
            (2.25, "zwee Mark a fënnefanzwanzeg Pfennig"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='currency', currency='DEM'), word)


    def test_year(self):
        test_cases = [
            (1000, "dausend"),
            (1100, "eelefhonnert"),
            (1200, "zwielefhonnert"),
            (1300, "dräizénghonnert"),
            (1400, "véierzénghonnert"),
            (1500, "fofzénghonnert"),
            (1600, "siechzénghonnert"),
            (1700, "siwwenzénghonnert"),
            (1800, "uechtzénghonnert"),
            (1900, "nonzénghonnert"),
            (1901, "nonzénghonnerteen"),
            (1902, "nonzénghonnertzwee"),
            (1910, "nonzénghonnertzéng"),
            (1919, "nonzénghonnertnonzéng"),
            (1920, "nonzénghonnertzwanzeg"),
            (1930, "nonzénghonnertdrësseg"),
            (1940, "nonzénghonnertvéierzeg"),
            (1950, "nonzénghonnertfofzeg"),
            (1960, "nonzénghonnertsechzeg"),
            (1970, "nonzénghonnertsiwwenzeg"),
            (1980, "nonzénghonnertachtzeg"),
            (1990, "nonzénghonnertnonzeg"),
            (1999, "nonzénghonnertnéngannonzeg"),
            (2000, "zweedausend"),
            (2001, "zweedausendeent"),
            (2010, "zweedausendzéng"),
            (2020, "zweedausendzwanzeg"),
            (2023, "zweedausenddräianzwanzeg"),
            (2100, "zweedausendeenhonnert"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='year'), word)

    def test_decimal(self):
        test_cases = [
            (0.0, "null Komma null"),
            (0.1, "null Komma eent"),
            (0.2, "null Komma zwee"),
            (0.5, "null Komma fënnef"),
            (0.10, "null Komma eent"),
            (0.25, "null Komma fënnefanzwanzeg"),
            (1.0, "eent Komma null"),
            (1.1, "eent Komma eent"),
            (1.2, "eent Komma zwee"),
            (1.3, "eent Komma dräi"),
            (1.4, "eent Komma véier"),
            (1.5, "eent Komma fënnef"),
            (1.6, "eent Komma sechs"),
            (1.7, "eent Komma siwen"),
            (1.8, "eent Komma aacht"),
            (1.9, "eent Komma néng"),
            (1.10, "eent Komma eent"),
            (1.11, "eent Komma eelef"),
            (1.12, "eent Komma zwielef"),
            (1.13, "eent Komma dräizéng"),
            (1.14, "eent Komma véierzéng"),
            (1.15, "eent Komma fofzéng"),
            (1.16, "eent Komma siechzéng"),
            (1.17, "eent Komma siwwenzéng"),
            (1.18, "eent Komma uechtzéng"),
            (1.19, "eent Komma nonzéng"),
            (1.20, "eent Komma zwanzeg"),
            (1.25, "eent Komma fënnefanzwanzeg"),
            (1.50, "eent Komma fofzeg"),
            (1.99, "eent Komma néng néng"),
            (2.0, "zwee Komma null"),
            (2.1, "zwee Komma eent"),
            (2.25, "zwee Komma fënnefanzwanzeg"),
            (10.5, "zéng Komma fënnef"),
            (100.25, "honnert Komma zwee fënnef"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb'), word)

    def test_negative(self):
        test_cases = [
            (-0, "null"),
            (-1, "minus eent"),
            (-2, "minus zwee"),
            (-3, "minus dräi"),
            (-10, "minus zéng"),
            (-11, "minus eelef"),
            (-12, "minus zwielef"),
            (-13, "minus dräizéng"),
            (-14, "minus véierzéng"),
            (-15, "minus fofzéng"),
            (-16, "minus siechzéng"),
            (-17, "minus siwwenzéng"),
            (-18, "minus uechtzéng"),
            (-19, "minus nonzéng"),
            (-20, "minus zwanzeg"),
            (-21, "minus eenanzwanzeg"),
            (-22, "minus zweeanzwanzeg"),
            (-30, "minus drësseg"),
            (-31, "minus eenandrësseg"),
            (-40, "minus véierzeg"),
            (-50, "minus fofzeg"),
            (-60, "minus sechzeg"),
            (-70, "minus siwwenzeg"),
            (-80, "minus achtzeg"),
            (-90, "minus nonzeg"),
            (-100, "minus honnert"),
            (-101, "minus honnerteent"),
            (-200, "minus zweehonnert"),
            (-1000, "minus dausend"),
            (-1001, "minus dausendeent"),
            (-2000, "minus zweedausend"),
            (-1.5, "minus eent Komma fënnef"),
            (-2.25, "minus zwee Komma fënnefanzwanzeg"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb'), word)

    def test_percentage(self):
        test_cases = [
            (0, "null Prozent"),
            (1, "ee Prozent"),
            (5, "fënnef Prozent"),
            (10, "zéng Prozent"),
            (25, "fënnefanzwanzeg Prozent"),
            (50, "fofzeg Prozent"),
            (75, "fënnefasiwwenzeg Prozent"),
            (100, "honnert Prozent"),
            (0.5, "null Komma fënnef Prozent"),
            (1.25, "eent Komma zwee fënnef Prozent"),
            (25.5, "fënnefanzwanzeg Komma fënnef Prozent"),
        ]

        for number, word in test_cases:
            self.assertEqual(self.n2w.to_percentage(number), word)

    def test_percentage_string(self):
        test_cases = [
            ("0%", "null Prozent"),
            ("1%", "ee Prozent"),
            ("25%", "fënnefanzwanzeg Prozent"),
            ("50%", "fofzeg Prozent"),
            ("75%", "fënnefasiwwenzeg Prozent"),
            ("100%", "honnert Prozent"),
            ("0.5%", "null Komma fënnef Prozent"),
            ("1.25%", "eent Komma zwee fënnef Prozent"),
        ]

        for number, word in test_cases:
            self.assertEqual(self.n2w.to_percentage(number), word)

    def test_unit_conversion(self):
        # Test temperature
        self.assertEqual(self.n2w.to_unit("90°"), "nonzeg Grad")
        self.assertEqual(self.n2w.to_unit("21°"), "eenanzwanzeg Grad")
        self.assertEqual(self.n2w.to_unit("0°"), "null Grad")
        self.assertEqual(self.n2w.to_unit("100°"), "honnert Grad")
        self.assertEqual(self.n2w.to_unit("-10°"), "minus zéng Grad")
        self.assertEqual(self.n2w.to_unit("-1°"), "minus een Grad")

        # Test weight (kg)
        self.assertEqual(self.n2w.to_unit("1kg"), "ee Kilogramm")
        self.assertEqual(self.n2w.to_unit("50 kg"), "fofzeg Kilogramm")
        self.assertEqual(self.n2w.to_unit("100kg"), "honnert Kilogramm")

        # Test volume (ml)
        self.assertEqual(self.n2w.to_unit("1ml"), "ee Milliliter")
        self.assertEqual(self.n2w.to_unit("50 ml"), "fofzeg Milliliter")
        self.assertEqual(self.n2w.to_unit("100ml"), "honnert Milliliter")

        # Test weight (gr)
        self.assertEqual(self.n2w.to_unit("1gr"), "ee Gramm")
        self.assertEqual(self.n2w.to_unit("50 gr"), "fofzeg Gramm")
        self.assertEqual(self.n2w.to_unit("100gr"), "honnert Gramm")

        # Test percentage
        self.assertEqual(self.n2w.to_unit("10%"), "zéng Prozent")
        self.assertEqual(self.n2w.to_unit("25 %"), "fënnefanzwanzeg Prozent")
        self.assertEqual(self.n2w.to_unit("50%"), "fofzeg Prozent")
        self.assertEqual(self.n2w.to_unit("75%"), "fënnefasiwwenzeg Prozent")
        self.assertEqual(self.n2w.to_unit("100 %"), "honnert Prozent")

        # Test years with -er suffix
        self.assertEqual(self.n2w.to_unit("1970er"), "nonzénghonnertsiwwenzeger")
        self.assertEqual(self.n2w.to_unit("1980er"), "nonzénghonnertachtzeger")
        self.assertEqual(self.n2w.to_unit("1990er"), "nonzénghonnertnonzeger")
        self.assertEqual(self.n2w.to_unit("2000er"), "zweedausender")
        self.assertEqual(self.n2w.to_unit("2020er"), "zweedausendzwanzeger")

    def test_unit_conversion_mixed_text(self):
        # Test mixed text with units
        text = "Et ass 30° haut an ech hunn 500ml Waasser gedronk"
        expected = "Et ass drësseg Grad haut an ech hunn fënnefhonnert Milliliter Waasser gedronk"
        self.assertEqual(self.n2w.to_unit(text), expected)

        text = "Am Joer 1970er waren et 25% méi waarm"
        expected = "Am Joer nonzénghonnertsiwwenzeger waren et fënnefanzwanzeg Prozent méi waarm"
        self.assertEqual(self.n2w.to_unit(text), expected)

        text = "D'Paquet weit 500gr an et kosts 2.50 Euro"
        expected = "D'Paquet weit fënnefhonnert Gramm an et kosts 2.50 Euro"
        self.assertEqual(self.n2w.to_unit(text), expected)

    def test_str_to_number(self):
        self.assertEqual(self.n2w.str_to_number("1"), 1)
        self.assertEqual(self.n2w.str_to_number("1,5"), 1.5)
        self.assertEqual(self.n2w.str_to_number(" 2.5 "), 2.5)
        self.assertEqual(self.n2w.str_to_number("0"), 0)
        self.assertEqual(self.n2w.str_to_number("-1"), -1)

    def test_merge_method(self):
        # Test merge method for compound number formation
        # (ctext, cnum, ntext, nnum)


        result = self.n2w.merge(("zwee", 2), ("honnert", 100))
        self.assertEqual(result, ("zweehonnert", 200))



        result = self.n2w.merge(("zwee", 2), ("Millioun", 1000000))
        self.assertEqual(result, ("zwee Milliounen", 2000000))

    def test_error_messages(self):
        # Test error message setup
        self.assertEqual(self.n2w.negword, "minus ")
        self.assertEqual(self.n2w.pointword, "Komma")
        self.assertIn("Gleitkommazahl", self.n2w.errmsg_floatord)
        self.assertIn("Nur Zahlen", self.n2w.errmsg_nonnum)
        self.assertIn("negative Zahl", self.n2w.errmsg_negord)
        self.assertIn("kleiner als", self.n2w.errmsg_toobig)

    def test_high_numbers(self):
        # Test high number words setup
        self.assertIn("zent", self.n2w.high_numwords)
        self.assertIn("illiard", self.n2w.GIGA_SUFFIX)
        self.assertIn("illioun", self.n2w.MEGA_SUFFIX)

    def test_mid_numwords(self):
        # Test mid number words (tens and hundreds)
        mid_words = dict(self.n2w.mid_numwords)
        self.assertEqual(mid_words[1000], "dausend")
        self.assertEqual(mid_words[100], "honnert")
        self.assertEqual(mid_words[90], "nonzeg")
        self.assertEqual(mid_words[80], "achtzeg")
        self.assertEqual(mid_words[70], "siwwenzeg")
        self.assertEqual(mid_words[60], "sechzeg")
        self.assertEqual(mid_words[50], "fofzeg")
        self.assertEqual(mid_words[40], "véierzeg")
        self.assertEqual(mid_words[30], "drësseg")

    def test_low_numwords(self):
        # Test low number words (0-20)
        self.assertEqual(self.n2w.low_numwords[0], "zwanzeg")  # 20
        self.assertEqual(self.n2w.low_numwords[1], "nonzéng")  # 19
        self.assertEqual(self.n2w.low_numwords[2], "uechtzéng")  # 18
        self.assertEqual(self.n2w.low_numwords[3], "siwwenzéng")  # 17
        self.assertEqual(self.n2w.low_numwords[4], "siechzéng")  # 16
        self.assertEqual(self.n2w.low_numwords[5], "fofzéng")  # 15
        self.assertEqual(self.n2w.low_numwords[6], "véierzéng")  # 14
        self.assertEqual(self.n2w.low_numwords[7], "dräizéng")  # 13
        self.assertEqual(self.n2w.low_numwords[8], "zwielef")  # 12
        self.assertEqual(self.n2w.low_numwords[9], "eelef")  # 11
        self.assertEqual(self.n2w.low_numwords[10], "zéng")  # 10
        self.assertEqual(self.n2w.low_numwords[11], "néng")  # 9
        self.assertEqual(self.n2w.low_numwords[12], "aacht")  # 8
        self.assertEqual(self.n2w.low_numwords[13], "siwen")  # 7
        self.assertEqual(self.n2w.low_numwords[14], "sechs")  # 6
        self.assertEqual(self.n2w.low_numwords[15], "fënnef")  # 5
        self.assertEqual(self.n2w.low_numwords[16], "véier")  # 4
        self.assertEqual(self.n2w.low_numwords[17], "dräi")  # 3
        self.assertEqual(self.n2w.low_numwords[18], "zwee")  # 2
        self.assertEqual(self.n2w.low_numwords[19], "eent")  # 1
        self.assertEqual(self.n2w.low_numwords[20], "null")  # 0

    def test_ordinal_transformations(self):
        # Test ordinal suffix transformations
        self.assertEqual(self.n2w.ords["eent"], "éischt")
        self.assertEqual(self.n2w.ords["dräi"], "drët")
        self.assertEqual(self.n2w.ords["aacht"], "aach")
        self.assertEqual(self.n2w.ords["siwen"], "siwen")
        self.assertEqual(self.n2w.ords["eg"], "egs")
        self.assertEqual(self.n2w.ords["ert"], "erts")
        self.assertEqual(self.n2w.ords["end"], "ends")
        self.assertEqual(self.n2w.ords["ioun"], "iouns")
        self.assertEqual(self.n2w.ords["nen"], "ns")
        self.assertEqual(self.n2w.ords["rde"], "rds")
        self.assertEqual(self.n2w.ords["rden"], "rds")

    def test_currency_parts(self):
        # Test currency parts parsing
        left, right, is_negative = self.n2w._get_currency_parts(1.25)
        self.assertEqual(left, 1)
        self.assertEqual(right, 25)
        self.assertFalse(is_negative)

        left, right, is_negative = self.n2w._get_currency_parts(-2.50)
        self.assertEqual(left, 2)
        self.assertEqual(right, 50)
        self.assertTrue(is_negative)

        left, right, is_negative = self.n2w._get_currency_parts(0.01)
        self.assertEqual(left, 0)
        self.assertEqual(right, 1)
        self.assertFalse(is_negative)

    def test_edge_cases(self):
        # Test edge cases and boundary conditions
        self.assertEqual(num2words(0, lang='lb'), "null")
        self.assertEqual(num2words(1, lang='lb'), "een")
        self.assertEqual(num2words(2, lang='lb'), "zwee")
        
        # Test large numbers
        self.assertIn("Millioun", num2words(1000000, lang='lb'))
        self.assertIn("Milliard", num2words(1000000000, lang='lb'))
        
        # Test zero handling
        self.assertEqual(self.n2w.to_cardinal(0), "null")
        self.assertEqual(self.n2w.to_ordinal(1), "eensten")

    def test_unsupported_currency(self):
        # Test error handling for unsupported currency
        with self.assertRaises(NotImplementedError):
            self.n2w.to_currency(1.00, currency='XYZ')

    def test_percentage_error_handling(self):
        # Test error handling for invalid percentage
        with self.assertRaises(ValueError):
            self.n2w.to_percentage("invalid")


if __name__ == '__main__':
    unittest.main() 