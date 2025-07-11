num2words library - Luxembourgish Number and Text Normalization
==================================================================



This repository contains an enhanced version of ``num2words`` with comprehensive Luxembourgish language support, including a powerful text normalizer for converting numbers, dates, times, and other numerical expressions to Luxembourgish text.

**⚠️ Important:** This Luxembourgish-enhanced version is only available from this GitHub repository and is not available on PyPI.

Installation
------------

Since this Luxembourgish-enhanced version is not available on PyPI, you must install it directly from this GitHub repository:

.. code-block:: bash

    git clone https://github.com/PeterGilles/num2words.git
    cd num2words
    pip install -e .

Or install directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/PeterGilles/num2words.git

Luxembourgish Language Support
-----------------------------

This version includes comprehensive Luxembourgish language support with the following features:

**Language Code:** ``lb`` (Luxembourgish)

Basic Usage
----------

Supported ``to`` options:

- ``cardinal`` (default): Convert to cardinal numbers (e.g., 42 → zweeavéierzeg)
- ``ordinal``: Convert to ordinal numbers (e.g., 42 → zweeavéierzegsten)
- ``ordinal_num``: Convert to ordinal numbers as numerals (e.g., 42 → 42.)
- ``year``: Convert to year form (e.g., 2023 → zweedausenddräianzwanzeg)
- ``currency``: Convert to currency form (e.g., 1.50 EUR → eent Euro an fofzeg Cent)

Command line with Luxembourgish:

.. code-block:: bash

    $ num2words 10001 -l lb
    dausendeent
    $ num2words 24,120.10 -l lb
    véieranzwanzegdausendhonnertzwanzeg Komma zéng
    $ num2words 24,120.35 -l lb
    véieranzwanzegdausendhonnertzwanzeg Komma fënnefandrësseg
    $ num2words 24.120,35 -l lb
    véieranzwanzegdausendhonnertzwanzeg Komma fënnefandrësseg
    $ num2words 1,234.56 -l lb
    dausendzweehonnertvéierandrësseg Komma sechsafofzeg
    $ num2words 1.234,56 -l lb
    dausendzweehonnertvéierandrësseg Komma sechsafofzeg

Note: Both English-style (comma as thousands, dot as decimal) and European-style (dot as thousands, comma as decimal) number formats are supported for all decimal and large number conversions.

In Python code:

.. code-block:: python

    >>> from num2words import num2words
    >>> num2words(42, lang='lb')
    'zweeavéierzeg'
    >>> num2words(42, lang='lb', to='ordinal')
    'zweeavéierzegsten'
    >>> num2words(2023, lang='lb', to='year')
    'zweedausenddräianzwanzeg'

Luxembourgish Text Normalizer
-----------------------------

The repository includes a comprehensive text normalizer (`luxembourgish_normalizer.py`) that converts various numerical expressions in Luxembourgish text to their word forms.

Installation and Usage:

.. code-block:: bash

    python luxembourgish_normalizer.py input_file.txt
    # or
    echo "Your text here" | python luxembourgish_normalizer.py

Supported Normalization Types
----------------------------

The Luxembourgish normalizer script (`luxembourgish_normalizer.py`) recognizes and converts the following types of expressions:

1. **Numbers and Large Numbers**
   - Recognizes: Standalone numbers, numbers with spaces or dots as thousand separators, numbers with decimals (dot or comma)
   - Converts: All numbers to their full Luxembourgish word form
   - Examples:
     - ``42`` → ``zweeavéierzeg``
     - ``1 234`` → ``dausendzweehonnertvéierandrësseg``
     - ``40 000`` → ``véierzegdausend``
     - ``24,120.35`` → ``véieranzwanzegdausendhonnertzwanzeg Komma fënnefandrësseg``
     - ``24.120,35`` → ``véieranzwanzegdausendhonnertzwanzeg Komma fënnefandrësseg``
     - ``1.234,56`` → ``dausendzweehonnertvéierandrësseg Komma sechsafofzeg``

2. **Dates and Ordinals**
   - Recognizes: Full dates, numeric dates, ordinals with dot
   - Converts: Dates to Luxembourgish with correct ordinal and month, ordinals to correct form before nouns
   - Examples:
     - ``30. Abrëll 2010`` → ``drëssegsten Abrëll zweedausendzéng``
     - ``22.3.`` → ``zweeanzwanzegste Mäerz``
     - ``9. Plaz`` → ``néngte Plaz``
     - ``den 1. Juni`` → ``den éischte Juni``
     - ``de 4. Juni`` → ``de véierte Juni``

3. **Times**
   - Recognizes: Times in ``HH:MM``, ``HHhMM``, or ``HH.MM`` format
   - Converts: To ``[hour] Auer [minute]`` in Luxembourgish, only for valid times (hours 0–24, minutes 0–59)
   - Examples:
     - ``10:34`` → ``zéng Auer véierandrësseg``
     - ``10h34`` → ``zéng Auer véierandrësseg``
     - ``17.40`` → ``siwwenzéng Auer véierzeg``
     - ``8:15`` → ``aacht Auer fofzéng``

4. **Match Results**
   - Recognizes: Sports scores in ``X:Y`` or ``X-Y`` format
   - Converts: To ``[score1] zu [score2]`` using correct Luxembourgish number words
   - Examples:
     - ``1:1`` → ``eent zu eent``
     - ``2:0`` → ``zwee zu null``
     - ``71:56`` → ``eenasiwwenzeg zu sechsafofzeg``
     - ``3-2`` → ``dräi zu zwee``

5. **Percentages**
   - Recognizes: Numbers followed by ``%`` (with or without space)
   - Converts: To ``[number] Prozent`` with correct decimal handling
   - Examples:
     - ``25%`` → ``fënnefanzwanzeg Prozent``
     - ``93,9%`` → ``dräiannonzeg Komma néng Prozent``
     - ``50 %`` → ``fofzeg Prozent``
     - ``1,25%`` → ``eent Komma fënnefanzwanzeg Prozent``

6. **Units and Measurements**
   - Recognizes: Numbers with units (temperature, volume, weight, distance, time)
   - Converts: To full Luxembourgish with correct unit and number form, including feminine forms
   - Examples:
     - ``90°`` → ``nonzeg Grad``
     - ``50 kg`` → ``fofzeg Kilogramm``
     - ``100 ml`` → ``honnert Milliliter``
     - ``60 km`` → ``sechzeg Kilometer``
     - ``2 Stonnen`` → ``zwou Stonnen``
     - ``1ml`` → ``ee Milliliter``
     - ``500 gr`` → ``fënnefhonnert Gramm``

7. **Phone Numbers**
   - Recognizes: Lines containing ``Telefon``, ``Tel``, or ``Phone`` with digit groups
   - Converts: Each digit to word, always including ``null`` for zeros and leading zeros
   - Examples:
     - ``Tel: 08 123 456`` → ``Tel: null aacht eent zwee dräi véier fënnef sechs``
     - ``Telefon: 352 123 456`` → ``Telefon: dräi fënnef zwee eent zwee dräi véier fënnef sechs``

8. **Abbreviations**
   - Recognizes: 2+ consecutive uppercase letters
   - Converts: To Luxembourgish letter pronunciation, or as a word if in custom dictionary
   - Examples:
     - ``VW`` → ``FAUWEE``
     - ``CSV`` → ``ZEEÄSSFAU``
     - ``FIFA`` → ``FIFA`` (custom dictionary word)
     - ``NATO`` → ``NATO`` (custom dictionary word)

9. **Years with Suffixes**
   - Recognizes: Decades like ``1970er``, ``80er``
   - Converts: To full Luxembourgish decade form
   - Examples:
     - ``1970er`` → ``nonzénghonnertsiwwenzeger``
     - ``1980er`` → ``nonzénghonnertachtzeger``
     - ``80er`` → ``achtzeger``
     - ``an den 1970er Joren`` → ``an den nonzénghonnertsiwwenzeger Joren``

10. **Currency**
    - Recognizes: Numbers with currency codes or symbols (EUR, €, USD, $, GBP, £, etc.)
    - Converts: To full Luxembourgish currency form with correct grammar
    - Examples:
      - ``1,50 EUR`` → ``een Euro a fofzeg Cent``
      - ``1,50€`` → ``een Euro a fofzeg Cent``
      - ``1.50 EUR`` → ``een Euro a fofzeg Cent``
      - ``2,25 USD`` → ``zwee Dollar a fënnefanzwanzeg Cent``
      - ``1,01 GBP`` → ``ee Pond an ee Penny``
      - ``huet 1,50 EUR kritt`` → ``huet een Euro a fofzeg Cent kritt``

Each normalization type is context-aware and applies Luxembourgish grammar and phonological rules for natural, correct output. The normalizer handles both European-style (comma as decimal) and English-style (dot as decimal) number formats.
