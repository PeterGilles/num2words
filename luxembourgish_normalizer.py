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

    def normalize_ordinal_dates(self, text):
        """Handle ordinal dates like '6. Abrëll' without year"""
        def ordinal_date_repl(match):
            article = match.group('article') or ''
            day = int(match.group('day'))
            month = match.group('month').lower()
            month_name = self.months.get(month, month.capitalize())
            day_ordinal = self.lb.to_ordinal(day)
            day_ordinal = self.adjust_ordinal_for_following_word(day_ordinal, month_name)
            return f"{article}{day_ordinal} {month_name}"

        # Pattern for ordinal dates without year: 6. Abrëll, 7. Plaz, etc.
        ordinal_date_pattern = re.compile(
            r'(?P<article>(?:dem |den |de |déi |an dësen )?)'
            r'(?P<day>\d{1,2})\. ?'
            r'(?P<month>[A-Za-zäëöüÄËÖÜ]+)'
        )
        text = ordinal_date_pattern.sub(ordinal_date_repl, text)
        
        # Handle numeric month format like '22.3.' (22nd of March)
        def numeric_month_repl(match):
            day = int(match.group('day'))
            month_num = int(match.group('month'))
            month_names = list(self.months.values())
            if 1 <= month_num <= 12:
                month_name = month_names[month_num - 1]
            else:
                month_name = f"Monat {month_num}"
            day_ordinal = self.lb.to_ordinal(day)
            day_ordinal = self.adjust_ordinal_for_following_word(day_ordinal, month_name)
            return f"{day_ordinal} {month_name}"
        
        # Pattern for DD.M format: 22.3. (22nd of March)
        numeric_month_pattern = re.compile(
            r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.'
        )
        text = numeric_month_pattern.sub(numeric_month_repl, text)
        
        return text

    def normalize_phone_numbers(self, text):
        """Convert phone numbers like '62 11 08' to words, always including 'null' for 0 and for leading zeros in groups like '08'."""
        def phone_repl(match):
            num = match.group(0)
            words = []
            for digit in num:
                if digit == '0':
                    words.append('null')
                else:
                    words.append(self.lb.to_cardinal(int(digit)))
            return " ".join(words)

        # For each line, if it looks like a phone number (contains "Telefon:" or similar), convert all groups of 2+ digits
        def phone_line_repl(line):
            if 'Telefon' in line or 'Tel' in line or 'Phone' in line:
                # Replace all groups of 2+ digits, even if followed by punctuation
                return re.sub(r'\d{2,}', phone_repl, line)
            return line
        text = '\n'.join(phone_line_repl(line) for line in text.splitlines())
        return text

    def normalize_units(self, text):
        # °, ml, gr, %, Minutten, Stonnen, Kilometer, etc.
        text = re.sub(r'(\d+)\s*°', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Grad", text)
        text = re.sub(r'(\d+)\s*ml', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Milliliter", text)
        text = re.sub(r'(\d+)\s*gr', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Gramm", text)
        
        # Handle decimal percentages with commas (e.g., 93,9%) or with space (e.g., 3,9 %)
        def percent_repl(match):
            percent_str = match.group(1)
            percent_val = percent_str.replace(',', '.')
            return self.lb.to_percentage(percent_val)
        text = re.sub(r'(\d+[,.]\d+)\s*%', percent_repl, text)
        # Handle whole number percentages with optional space
        text = re.sub(r'(\d+)\s*%', lambda m: f"{self.lb.to_cardinal(int(m.group(1)))} Prozent", text)
        
        # Handle whole number percentages
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
        """Convert time expressions like 10:34, 10h34, or 17.40 to Luxembourgish text, avoiding duplicate 'Auer' if already present and not appending 'Auer' after minutes if already present in the input."""
        
        def insert_auer(hours_word, minutes_word, original, match_start, match_end):
            # Only insert 'Auer' if not already present after the match
            after = original[match_end:match_end+6].lower()
            # If 'Auer' is present after the match, do not append 'Auer' after minutes
            if 'auer' in after:
                return f"{hours_word} Auer {minutes_word}"
            else:
                return f"{hours_word} Auer {minutes_word}"

        # Handle 17.40 format (time with dot)
        def time_dot_repl(match):
            hours = int(match.group(1))
            minutes = int(match.group(2))
            hours_word = "null" if hours == 0 else ("eng" if hours == 1 else self.lb.to_cardinal(hours))
            minutes_word = "null" if minutes == 0 else self.lb.to_cardinal(minutes)
            # Check if 'Auer' is present after the match
            after = match.string[match.end():match.end()+6].lower()
            if 'auer' in after:
                return f"{hours_word} Auer {minutes_word}"
            else:
                return f"{hours_word} Auer {minutes_word}"
        # Only match valid times: hours 0-24, minutes 00-59
        time_dot_pattern = re.compile(r'\b([01]?\d|2[0-4])\.(?:[0-5]\d)\b')
        text = time_dot_pattern.sub(time_dot_repl, text)

        # Handle 10:34 format
        def time_repl(match):
            hours = int(match.group(1))
            minutes = int(match.group(2))
            hours_word = "null" if hours == 0 else ("eng" if hours == 1 else self.lb.to_cardinal(hours))
            minutes_word = "null" if minutes == 0 else self.lb.to_cardinal(minutes)
            after = match.string[match.end():match.end()+6].lower()
            if 'auer' in after:
                return f"{hours_word} Auer {minutes_word}"
            else:
                return f"{hours_word} Auer {minutes_word}"
        time_pattern = re.compile(r'\b([01]?\d|2[0-4]):([0-5]\d)\b')
        text = time_pattern.sub(time_repl, text)

        # Handle 10h34 format
        def time_h_repl(match):
            hours = int(match.group(1))
            minutes = int(match.group(2))
            hours_word = "null" if hours == 0 else ("eng" if hours == 1 else self.lb.to_cardinal(hours))
            minutes_word = "null" if minutes == 0 else self.lb.to_cardinal(minutes)
            after = match.string[match.end():match.end()+6].lower()
            if 'auer' in after:
                return f"{hours_word} Auer {minutes_word}"
            else:
                return f"{hours_word} Auer {minutes_word}"
        time_h_pattern = re.compile(r'\b([01]?\d|2[0-4])h([0-5]\d)\b')
        text = time_h_pattern.sub(time_h_repl, text)

        # Remove duplicate 'Auer' if it appears twice in a row
        text = re.sub(r'(Auer)\s+\1', r'\1', text)
        # Remove 'Auer' after minutes if it appears (e.g., 'siwwenzéng Auer véierzeg Auer' -> 'siwwenzéng Auer véierzeg')
        text = re.sub(r'(Auer [^\s]+) Auer', r'\1', text)
        return text

    def normalize_large_numbers(self, text):
        """Handle large numbers like 2.000 and 40 000"""
        def large_number_repl(match):
            number_str = match.group(1).replace('.', '').replace(' ', '')
            number = int(number_str)
            return self.lb.to_cardinal(number)
        
        # Pattern for numbers with dots or spaces as thousand separators
        large_number_pattern = re.compile(r'\b(\d{1,3}(?:[\.\s]\d{3})+)\b')
        text = large_number_pattern.sub(large_number_repl, text)
        return text

    def normalize_large_number_words(self, text):
        """Handle large number words like '961 Milliarden'"""
        def large_word_repl(match):
            number = int(match.group(1))
            unit = match.group(2)
            number_word = self.lb.to_cardinal(number)
            
            # Handle different large number units
            if unit.lower() in ['milliarden', 'milliard']:
                if number == 1:
                    return f"{number_word} Milliard"
                else:
                    return f"{number_word} Milliarden"
            elif unit.lower() in ['milliounen', 'millioun']:
                if number == 1:
                    return f"{number_word} Millioun"
                else:
                    return f"{number_word} Milliounen"
            else:
                return f"{number_word} {unit}"
        
        # Pattern for number + large unit (e.g., 961 Milliarden)
        large_word_pattern = re.compile(r'(\d+)\s+(Milliarden?|Milliounen?)', re.IGNORECASE)
        text = large_word_pattern.sub(large_word_repl, text)
        return text

    def normalize_match_results(self, text):
        # Convert match results like 1:1 or 1-1 to 'eent zu eent'
        def match_result_repl(match):
            left = int(match.group(1))
            right = int(match.group(2))
            left_word = 'eent' if left == 1 else self.lb.to_cardinal(left)
            right_word = 'eent' if right == 1 else self.lb.to_cardinal(right)
            return f"{left_word} zu {right_word}"
        # Match numbers 0-999 for sports scores (basketball, handball, etc.)
        return re.sub(r'\b(\d{1,3})[:\-](\d{1,3})\b', match_result_repl, text)

    def normalize_abbreviations(self, text):
        """Convert abbreviations like VW, CSV to their Luxembourgish letter pronunciations"""
        # Luxembourgish letter pronunciations
        letter_pronunciations = {
            'A': 'AA', 'B': 'BEE', 'C': 'ZEE', 'D': 'DEE', 'E': 'EE',
            'F': 'ÄFF', 'G': 'GEE', 'H': 'HASCH', 'I': 'I', 'J': 'JOTT',
            'K': 'KA', 'L': 'ÄLL', 'M': 'ÄMM', 'N': 'ÄNN', 'O': 'O',
            'P': 'PEE', 'Q': 'KU', 'R': 'ÄRR', 'S': 'ÄSS', 'T': 'TEE',
            'U': 'U', 'V': 'FAU', 'W': 'WEE', 'X': 'ICKS', 'Y': 'I-GRÄCK',
            'Z': 'ZÄTT', 'Ä': 'Ä', 'Ö': 'Ö', 'Ü': 'Ü'
        }
        
        # Custom dictionary for word-based abbreviations
        word_abbreviations = {
            'FIFA': 'FIFA',
            'NATO': 'NATO',
            'UNO': 'UNO',
            'EU': 'EU',
            'USA': 'USA',
            'UNESCO': 'UNESCO',
            'UNICEF': 'UNICEF',
            'WHO': 'WHO',
            'UN': 'UN',
            'EU': 'EU',
            'UNO': 'UNO'
        }
        
        def abbreviation_repl(match):
            abbreviation = match.group(0)
            
            # Check if it's a word-based abbreviation first
            if abbreviation in word_abbreviations:
                return word_abbreviations[abbreviation]
            
            # Convert each letter to its pronunciation
            pronunciations = []
            for letter in abbreviation:
                if letter in letter_pronunciations:
                    pronunciations.append(letter_pronunciations[letter])
                else:
                    # Keep unknown characters as-is
                    pronunciations.append(letter)
            return ''.join(pronunciations)
        
        # Match 2+ consecutive capital letters (abbreviations)
        # Exclude if followed by lowercase letters (part of a word)
        abbreviation_pattern = re.compile(r'\b[A-ZÄÖÜ]{2,}\b')
        text = abbreviation_pattern.sub(abbreviation_repl, text)
        return text

    def normalize(self, text):
        text = self.normalize_phone_numbers(text)  # Move phone numbers to the top
        text = self.normalize_abbreviations(text)  # Handle abbreviations early
        text = self.normalize_match_results(text)  # Handle match results before times
        text = self.normalize_dates(text)
        text = self.normalize_ordinal_dates(text)  # Add ordinal dates
        text = self.normalize_times(text)
        text = self.normalize_ordinal_dates(text)  # Run ordinal dates again after times
        text = self.normalize_large_numbers(text)  # Add large numbers
        text = self.normalize_large_number_words(text)  # Add large number words
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