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
            (30, "drësseg"),
            (31, "eenandrësseg"),
            (40, "véierzeg"),
            (41, "eenavéierzeg"),
            (50, "fofzeg"),
            (53, "dräiafofzeg"),
            (60, "sechzeg"),
            (64, "véierasechzeg"),
            (70, "siwwenzeg"),
            (75, "fënnefasiwwenzeg"),
            (80, "achtzeg"),
            (81, "eenanachtzeg"),
            (90, "nonzeg"),
            (91, "eenannonzeg"),
            (100, "eenhonnert"),
            (101, "eenhonnerteent"),
            (200, "zweehonnert"),
            (1000, "eendausend"),
            (1001, "eendausendeent"),
            (2000, "zweedausend"),
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
            (100, "eenhonnertsten"),
            (101, "eenhonnertéischten"),
            (200, "zweehonnertsten"),
            (1000, "eendausendsten"),
            (1001, "eendausendéischten"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='ordinal'), word)

    def test_currency(self):
        test_cases = [
            (1.00, "een Euro"),
            (2.00, "zwee Euro"),
            (1.01, "een Euro an een Cent"),
            (1.10, "een Euro an zéng Cent"),
            (1.21, "een Euro an eenanzwanzeg Cent"),
            (1.53, "een Euro an dräiafofzeg Cent"),
            (1.99, "een Euro an néngannonzeg Cent"),
            (2.00, "zwee Euro"),
            (2.01, "zwee Euro an een Cent"),
            (2.10, "zwee Euro an zéng Cent"),
            (2.21, "zwee Euro an eenanzwanzeg Cent"),
            (2.50, "zwee Euro a fofzeg Cent"),
            (2.99, "zwee Euro an néngannonzeg Cent"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='currency'), word)

    def test_year(self):
        test_cases = [
            (2023, "zweedausenddräianzwanzeg"),
            (2000, "zweedausend"),
            (1900, "nonzénghonnert"),
            (1800, "uechtzénghonnert"),
            (1700, "siwwenzénghonnert"),
            (1600, "siechzénghonnert"),
            (1500, "fofzénghonnert"),
            (1400, "véierzénghonnert"),
            (1300, "dräizénghonnert"),
            (1200, "zwielefhonnert"),
            (1100, "eelefhonnert"),
            (1000, "eendausend"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb', to='year'), word)

    def test_decimal(self):
        test_cases = [
            (1.0, "ee Komma null"),
            (1.1, "ee Komma eent"),
            (1.2, "ee Komma zwee"),
            (1.3, "ee Komma dräi"),
            (1.4, "ee Komma véier"),
            (1.5, "ee Komma fënnef"),
            (1.6, "ee Komma sechs"),
            (1.7, "ee Komma siwen"),
            (1.8, "ee Komma aacht"),
            (1.9, "ee Komma néng"),
            (1.10, "ee Komma zéng"),
            (1.11, "ee Komma eelef"),
            (1.12, "ee Komma zwielef"),
            (1.13, "ee Komma dräizéng"),
            (1.14, "ee Komma véierzéng"),
            (1.15, "ee Komma fofzéng"),
            (1.16, "ee Komma siechzéng"),
            (1.17, "ee Komma siwwenzéng"),
            (1.18, "ee Komma uechtzéng"),
            (1.19, "ee Komma nonzéng"),
            (1.20, "ee Komma zwanzeg"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb'), word)

    def test_negative(self):
        test_cases = [
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
            (-100, "minus eenhonnert"),
            (-101, "minus eenhonnerteent"),
            (-200, "minus zweehonnert"),
            (-1000, "minus eendausend"),
            (-1001, "minus eendausendeent"),
            (-2000, "minus zweedausend"),
        ]

        for number, word in test_cases:
            self.assertEqual(num2words(number, lang='lb'), word)


if __name__ == '__main__':
    unittest.main() 