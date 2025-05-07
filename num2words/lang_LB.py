# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import print_function, unicode_literals

import re

from .lang_EU import Num2Word_EU


class Num2Word_LB(Num2Word_EU):
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
        # "Cannot treat float %s as ordinal."
        self.errmsg_floatord = (
            "Die Gleitkommazahl %s kann nicht in eine Ordnungszahl " +
            "konvertiert werden."
            )
        # "type(((type(%s)) ) not in [long, int, float]"
        self.errmsg_nonnum = (
            "Nur Zahlen (type(%s)) können in Wörter konvertiert werden."
            )
        # "Cannot treat negative num %s as ordinal."
        self.errmsg_negord = (
            "Die negative Zahl %s kann nicht in eine Ordnungszahl " +
            "konvertiert werden."
            )
        # "abs(%s) must be less than %s."
        self.errmsg_toobig = "Die Zahl %s muss kleiner als %s sein."
        self.exclude_title = []

        lows = ["Non", "Okt", "Sept", "Sext", "Quint", "Quadr", "Tr", "B", "M"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept",
                 "okto", "novem"]
        tens = ["dez", "vigint", "trigint", "quadragint", "quinquagint",
                "sexagint", "septuagint", "oktogint", "nonagint"]
        self.high_numwords = (
            ["zent"] + self.gen_high_numwords(units, tens, lows)
        )
        self.mid_numwords = [(1000, "dausend"), (100, "honnert"),
                             (90, "nonnzeg"), (80, "achtzeg"), (70, "siwenzeg"),
                             (60, "sechzeg"), (50, "foffzeg"),
                             (40, "v\xE9ierzeg"), (30, "dr\xebsseg")]
        self.low_numwords = ["zwanzeg", "nonnzéng", "uechtzéng", "siwenzéng",
                             "siechzéng", "foffzéng", "v\xE9ierzéng", "dr\xe4izéng",
                             "zwielef", "eelef", "zéng", "néng", "aacht",
                             "siwen", "sechs", "f\xebnef", "v\xe9ier", "dr\xe4i",
                             "zwee", "eent", "null"]
        self.ords = {"eent": "\xe9scht",
                     "dr\xe4i": "dr\xe9t",
                     "aacht": "aach",
                     "siwen": "siwen",
                     "eg": "egs",
                     "ert": "erts",
                     "end": "ends",
                     "ioun": "iouns",
                     "nen": "ns",
                     "rde": "rds",
                     "rden": "rds"}

    def to_cardinal(self, number):
        if number < 0:
            return self.negword + self.to_cardinal(abs(number))
    
        if number == 0:
            return "null"
    
        units_map = {
            1: "een",
            2: "zwee",
            3: "dräi",
            4: "véier",
            5: "fënnef",
            6: "sechs",
            7: "siwen",
            8: "aacht",
            9: "néng"
        }
    
        tens_map = dict(self.mid_numwords)
    
        if 21 <= number <= 99 and number % 10 != 0:
            unit = number % 10
            ten = number - unit
            unit_word = units_map[unit]
            ten_word = tens_map.get(ten, "")
            joiner = "a" if ten_word.startswith(("véier", "fënnef", "foffzeg", "sech", "siwen")) else "an"
            return unit_word + joiner + ten_word
    
        # Special cases for 1–20 and multiples of 10
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
    
        return (ctext + ntext, cnum + nnum)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "."

    def to_currency(self, val, currency='EUR', cents=True, separator=' an',
                    adjective=False):
        result = super(Num2Word_DE, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)
        # Handle exception, in german is "ein Euro" and not "eins Euro"
        return result.replace("eent ", "een ")

    def to_year(self, val, longval=True):
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="honnert", longval=longval)\
            .replace(' ', '')
