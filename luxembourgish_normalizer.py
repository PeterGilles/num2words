#!/usr/bin/env python3
import re
from num2words.lang_LB import Num2Word_LB

class LuxembourgishNormalizer:
    def __init__(self):
        self.lb = Num2Word_LB()
        self.months = {
            'januar': 'Januar', 'februar': 'Februar', 'mäerz': 'Mäerz', 'abrëll': 'Abrëll',
            'mee': 'Mee', 'juni': 'Juni', 'juli': 'Juli', 'august': 'August',
            'september': 'September', 'oktober': 'Oktober', 'november': 'November', 'dezember': 'Dezember'
        }
        self.articles = ['den', 'de', 'um']

    def adjust_ordinal_for_following_word(self, ordinal, following_word):
        if not following_word:
            return ordinal
        first_letter = following_word[0].lower()
        if first_letter in 'aeiouäëöündtz':
            return ordinal
        if ordinal.endswith('n'):
            return ordinal[:-1]
        return ordinal

    def normalize_dates(self, text):
        # Handle articles before dates
        def date_repl(match):
            article = match.group('article') or ''
            day = int(match.group('day'))
            month = match.group('month').lower()
            year = int(match.group('year'))
            month_name = self.months.get(month, month.capitalize())
            day_ordinal = self.lb.to_ordinal(day)
            day_ordinal = self.adjust_ordinal_for_following_word(day_ordinal, month_name)
            year_text = self.lb.to_year(year)
            return f"{article}{day_ordinal} {month_name} {year_text}"

        # den 30. Abrëll 2010, de 15. Mee 1982, um 5. Juli 2021, 5. Juli 2021, etc.
        date_pattern = re.compile(
            r'(?P<article>(?:dem |den |de |um )?)'
            r'(?P<day>\d{1,2})\. ?'
            r'(?P<month>[A-Za-zäëöüÄËÖÜ]+) '
            r'(?P<year>\d{4})'
        )
        text = date_pattern.sub(date_repl, text)

        # Numeric date: den 28.11.1733, 28.11.1733, etc.
        def numeric_date_repl(match):
            article = match.group('article') or ''
            day = int(match.group('day'))
            month_num = int(match.group('month'))
            year = int(match.group('year'))
            month_names = list(self.months.values())
            month_name = month_names[month_num - 1] if 1 <= month_num <= 12 else f"Monat {month_num}"
            day_ordinal = self.lb.to_ordinal(day)
            day_ordinal = self.adjust_ordinal_for_following_word(day_ordinal, month_name)
            year_text = self.lb.to_year(year)
            return f"{article}{day_ordinal} {month_name} {year_text}"

        numeric_date_pattern = re.compile(
            r'(?P<article>(?:dem |den |de |um )?)'
            r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})'
        )
        text = numeric_date_pattern.sub(numeric_date_repl, text)

        # Month + year: Abrëll 1887, Oktober 1344, etc.
        def month_year_repl(match):
            article = match.group('article') or ''
            month = match.group('month').lower()
            year = int(match.group('year'))
            month_name = self.months.get(month, month.capitalize())
            year_text = self.lb.to_year(year)
            return f"{article}{month_name} {year_text}"

        month_year_pattern = re.compile(
            r'(?P<article>(?:dem |den |de |um )?)'
            r'(?P<month>[A-Za-zäëöüÄËÖÜ]+) '
            r'(?P<year>\d{4})'
        )
        text = month_year_pattern.sub(month_year_repl, text)

        return text

    def normalize_units(self, text):
        # °, ml, gr, %, Minutten, Stonnen, Kilometer, etc.
        text = re.sub(r'(\d+)\s*°', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Grad", text)
        text = re.sub(r'(\d+)\s*ml', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Milliliter", text)
        text = re.sub(r'(\d+)\s*gr', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Gramm", text)
        text = re.sub(r'(\d+)\s*%', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Prozent", text)
        text = re.sub(r'(\d+)\s*Minutten', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Minutten", text)
        
        # Special handling for feminine nouns
        def stonnen_repl(match):
            num = int(match.group(1))
            if num == 2:
                return "zwou Stonnen"
            else:
                return f"{self.lb.to_cardinal(num)} Stonnen"
        text = re.sub(r'(\d+)\s*Stonnen', stonnen_repl, text)
        
        # Handle other feminine nouns that might need special treatment
        feminine_nouns = {
            'Wochen': 'Woch',
            'Monaten': 'Mount', 
            'Stroossen': 'Strooss',
            'Fläschen': 'Fläsch',
            'Maschinnen': 'Maschinn'
        }
        
        for plural, singular in feminine_nouns.items():
            def feminine_repl(match):
                num = int(match.group(1))
                if num == 2:
                    return f"zwou {plural}"
                else:
                    return f"{self.lb.to_cardinal(num)} {plural}"
            text = re.sub(rf'(\d+)\s*{plural}', feminine_repl, text)
        
        text = re.sub(r'(\d+)\s*Kilometer', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Kilometer", text)
        # Singular fixes
        text = text.replace("eent Milliliter", "ee Milliliter")
        text = text.replace("eent Gramm", "ee Gramm")
        text = text.replace("eent Grad", "ee Grad")
        text = text.replace("eent Prozent", "ee Prozent")
        return text

    def normalize_years_with_suffix(self, text):
        # 1970er, 1980er, etc.
        def year_suffix_repl(match):
            year = int(match.group(1))
            try:
                year_text = self.lb.to_year(year)
            except AttributeError:
                year_text = self.lb.to_cardinal(year)
            return f"{year_text}er"
        return re.sub(r'\b(1\d{3}|20\d{2})er\b', year_suffix_repl, text)

    def normalize_numbers(self, text):
        # Standalone numbers (not part of dates/units)
        def number_repl(match):
            num = int(match.group(0))
            return self.lb.to_cardinal(num)
        # Only replace numbers not part of a word (avoid breaking years, units, etc.)
        return re.sub(r'\b\d+\b', number_repl, text)

    def normalize_times(self, text):
        """Convert time expressions like 10:34 or 10h34 to Luxembourgish text"""
        
        # Handle 10:34 format
        def time_repl(match):
            hours = int(match.group(1))
            minutes = int(match.group(2))
            
            # Convert hours to words
            if hours == 0:
                hours_word = "null"
            elif hours == 1:
                hours_word = "eng"
            else:
                hours_word = self.lb.to_cardinal(hours)
            
            # Convert minutes to words
            if minutes == 0:
                minutes_word = "null"
            else:
                minutes_word = self.lb.to_cardinal(minutes)
            
            return f"{hours_word} Auer {minutes_word}"
        
        # Pattern for HH:MM format
        time_pattern = re.compile(r'\b(\d{1,2}):(\d{2})\b')
        text = time_pattern.sub(time_repl, text)
        
        # Handle 10h34 format
        def time_h_repl(match):
            hours = int(match.group(1))
            minutes = int(match.group(2))
            
            # Convert hours to words
            if hours == 0:
                hours_word = "null"
            elif hours == 1:
                hours_word = "eng"
            else:
                hours_word = self.lb.to_cardinal(hours)
            
            # Convert minutes to words
            if minutes == 0:
                minutes_word = "null"
            else:
                minutes_word = self.lb.to_cardinal(minutes)
            
            return f"{hours_word} Auer {minutes_word}"
        
        # Pattern for HHhMM format
        time_h_pattern = re.compile(r'\b(\d{1,2})h(\d{2})\b')
        text = time_h_pattern.sub(time_h_repl, text)
        
        return text

    def normalize(self, text):
        text = self.normalize_dates(text)
        text = self.normalize_times(text)  # Add time normalization
        text = self.normalize_units(text)
        text = self.normalize_years_with_suffix(text)
        text = self.normalize_numbers(text)
        return text

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as f:
            input_text = f.read()
    else:
        input_text = sys.stdin.read()
    normalizer = LuxembourgishNormalizer()
    output_text = normalizer.normalize(input_text)
    print(output_text) 