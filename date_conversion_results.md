# Luxembourgish Date Conversion Results

## Test Results for Date Conversions (Corrected Ordinal Forms)

The following dates were successfully converted to Luxembourgish text using the num2words library with proper ordinal adjustment:

### Full Date Format (Day. Month Year)
- **30. Abrëll 2010** → drëssegsten Abrëll zweedausendzéng
- **21. Januar 1467** → eenanzwanzegste Januar dausendvéierhonnertsiwenasechzeg
- **15. Mee 1982** → fofzéngte Mee nonzénghonnertzweeanachtzeg
- **5. Juli 2021** → fënnefte Juli zweedausendeenanzwanzeg
- **24. Dezember 1965** → véieranzwanzegten Dezember nonzénghonnertfënnefasechzeg
- **5. Februar 2020** → fënnefte Februar zweedausendzwanzeg
- **30. September 1918** → drëssegste September nonzénghonnertuechtzéng
- **2. Mee 2022** → zweete Mee zweedausendzweeanzwanzeg
- **2. Mäerz 1604** → zweete Mäerz dausendsechshonnertvéier
- **1. Dezember 1541** → éischten Dezember dausendfënnefhonnerteenavéierzeg
- **4. Juli 1802** → véierte Juli dausendaachthonnertzwee
- **23. Oktober 1699** → dräianzwanzegsten Oktober dausendsechshonnertnéngannonzeg
- **4. Mee 1575** → véierte Mee dausendfënnefhonnertfënnefasiwwenzeg
- **10. Februar 1432** → zéngte Februar dausendvéierhonnertzweeandrësseg
- **2. Abrëll 1950** → zweeten Abrëll nonzénghonnertfofzeg
- **15. Oktober 2004** → fofzéngten Oktober zweedausendvéier
- **19. Mäerz 2019** → nonzéngte Mäerz zweedausendnonzéng

### Numeric Date Format (DD.MM.YYYY)
- **28.11.1733** → aachtanzwanzegsten November dausendsiwenhonnertdräiandrësseg
- **3.3.1844** → drëtte Mäerz dausendaachthonnertvéieravéierzeg
- **14.10.1999** → véierzéngten Oktober nonzénghonnertnéngannonzeg
- **5.8.1501** → fënneften August dausendfënnefhonnerteent
- **11.6.2003** → eelefte Juni zweedausenddräi
- **30.4.2018** → drëssegsten Abrëll zweedausenduechtzéng
- **8.2.2015** → aachte Februar zweedausendfofzéng
- **16.6.1492** → siechzéngte Juni dausendvéierhonnertzweeannonzeg
- **10.8.2013** → zéngten August zweedausenddräizéng
- **9.9.1990** → néngte September nonzénghonnertnonzeg
- **18.2.2024** → uechtzéngte Februar zweedausendvéieranzwanzeg
- **31.3.2011** → eenandrëssegste Mäerz zweedausendeelef
- **2.11.1900** → zweeten November nonzénghonnert
- **12.12.2012** → zwieleften Dezember zweedausendzwielef
- **7.6.1717** → siwente Juni dausendsiwenhonnertsiwwenzéng
- **14.1.1744** → véierzéngte Januar dausendsiwenhonnertvéieravéierzeg
- **1.5.1866** → éischte Mee dausendaachthonnertsechsasechzeg

### Month-Year Only Format
- **Mäerz 1756** → Mäerz dausendsiwenhonnertsechsafofzeg
- **Oktober 1344** → Oktober dausenddräihonnertvéieravéierzeg
- **Abrëll 1887** → Abrëll dausendaachthonnertsiwenanachtzeg
- **Januar 1977** → Januar nonzénghonnertsiwenasiwwenzeg

### Special Cases
- **6. 6.7.1940** → sechste Juli nonzénghonnertvéierzeg (handled double day format)

## Key Features

1. **Corrected Ordinal Day Numbers**: Days are converted to ordinal form with proper Luxembourgish grammar:
   - **With 'n'**: When followed by words starting with vowels or n, d, t, z (e.g., "drëssegsten Abrëll", "éischten Dezember")
   - **Without 'n'**: When followed by other consonants (e.g., "eenanzwanzegste Januar", "fënnefte Juli")

2. **Year Conversion**: Years are converted to full text using the `to_year()` method
3. **Month Names**: Preserved in Luxembourgish (Januar, Februar, Mäerz, etc.)
4. **Multiple Formats**: Handles various date formats including:
   - Day. Month Year (30. Abrëll 2010)
   - DD.MM.YYYY (28.11.1733)
   - Month Year only (Mäerz 1756)
   - Special formats with double day numbers

## Ordinal Adjustment Rules

The final 'n' in ordinal numbers is dropped when the following word doesn't start with:
- **Vowels**: a, e, i, o, u, ä, ë, ö, ü
- **Consonants**: n, d, t, z

**Examples:**
- "21. Januar" → "eenanzwanzegste Januar" (no 'n' because 'J' is not in the exception list)
- "30. Abrëll" → "drëssegsten Abrëll" (keeps 'n' because 'A' is a vowel)
- "5. Juli" → "fënnefte Juli" (no 'n' because 'J' is not in the exception list)
- "1. Dezember" → "éischten Dezember" (keeps 'n' because 'D' is in the exception list)

## Usage

The date converter can be used as follows:

```python
from num2words.lang_LB import Num2Word_LB

converter = DateConverter()
result = converter.convert_date("21. Januar 1467")
# Returns: "eenanzwanzegste Januar dausendvéierhonnertsiwenasechzeg"
```

All dates were successfully converted to proper Luxembourgish text format with correct ordinal grammar. 