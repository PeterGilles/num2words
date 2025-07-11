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
   - Converts: All numbers to their full Luxembourgish word form, e.g. ``42`` → ``zweeavéierzeg``, ``40 000`` → ``véierzegdausend``, ``24,120.35`` or ``24.120,35`` → ``véieranzwanzegdausendhonnertzwanzeg Komma fënnefandrësseg``

2. **Dates and Ordinals**
   - Recognizes: Full dates (e.g. ``30. Abrëll 2010``), numeric dates (e.g. ``22.3.``), ordinals with dot (e.g. ``9. Plaz``)
   - Converts: Dates to Luxembourgish with correct ordinal and month, ordinals to correct form before nouns

3. **Times**
   - Recognizes: Times in ``HH:MM``, ``HHhMM``, or ``HH.MM`` format (e.g. ``10:34``, ``10h34``, ``17.40``)
   - Converts: To ``[hour] Auer [minute]`` in Luxembourgish, only for valid times (hours 0–24, minutes 0–59)

4. **Match Results**
   - Recognizes: Sports scores in ``X:Y`` or ``X-Y`` format (e.g. ``1:1``, ``71:56``)
   - Converts: To ``[score1] zu [score2]`` using correct Luxembourgish number words (e.g. ``eent zu eent``, ``eenasiwwenzeg zu sechsafofzeg``)

5. **Percentages**
   - Recognizes: Numbers followed by ``%`` (e.g. ``25%``, ``93,9%``)
   - Converts: To ``[number] Prozent`` with correct decimal handling (e.g. ``dräiannonzeg Komma néng Prozent``)

6. **Units and Measurements**
   - Recognizes: Numbers with units (e.g. ``90°``, ``50 kg``, ``100 ml``, ``60 km``, ``2 Stonnen``)
   - Converts: To full Luxembourgish with correct unit and number form, including feminine forms (e.g. ``zwou Stonnen``)

7. **Phone Numbers**
   - Recognizes: Lines containing ``Telefon``, ``Tel``, or ``Phone`` with digit groups
   - Converts: Each digit to word, always including ``null`` for zeros and leading zeros (e.g. ``08`` → ``null aacht``)

8. **Abbreviations**
   - Recognizes: 2+ consecutive uppercase letters (e.g. ``VW``, ``CSV``, ``FIFA``)
   - Converts: To Luxembourgish letter pronunciation (e.g. ``FAUWEE``), or as a word if in a custom dictionary (e.g. ``FIFA``)

9. **Years with Suffixes**
   - Recognizes: Decades like ``1970er``
   - Converts: To full Luxembourgish decade form (e.g. ``nonzéngdausendsiwwenzénger``)

10. **Currency**
    - Recognizes: Numbers with currency codes (e.g. ``1,50 EUR``)
    - Converts: To full Luxembourgish currency form (e.g. ``eent Euro an fofzeg Cent``), with correct grammar

Each normalization type is context-aware and applies Luxembourgish grammar and phonological rules for natural, correct output.
