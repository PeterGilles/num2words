import pytest
from num2words.run_num2words import TextNormalizer
from num2words.lang_LB import Num2Word_LB

# --- Years and Decades with 'er' Suffix ---
@pytest.mark.parametrize("input_text,expected", [
    ("1970er", "nonzénghonnertsiwwenzeger"),
    ("1980er", "nonzénghonnertachtzeger"),
    ("1990er", "nonzénghonnertnonzeger"),
    ("2000er", "zweedausender"),
    ("2020er", "zweedausendzwanzeger"),
    ("80er", "achtzeger"),
    ("90er", "nonzeger"),
    ("In den 1970er bis 1990er Jahren", "In den nonzénghonnertsiwwenzeger bis nonzénghonnertnonzeger Jahren"),
])
def test_years_and_decades(input_text, expected):
    normalizer = TextNormalizer()
    assert normalizer.normalize_text(input_text) == expected

# --- Units: Temperature, Volume, Weight, Percentage ---
@pytest.mark.parametrize("input_text,expected", [
    ("90°", "nonzeg Grad"),
    ("21°", "eenanzwanzeg Grad"),
    ("0°", "null Grad"),
    ("100°", "honnert Grad"),
    ("Et huet 30° haut", "Et ass drësseg Grad haut"),
    ("1ml", "ee Milliliter"),
    ("50 ml", "fofzeg Milliliter"),
    ("100ml", "honnert Milliliter"),
    ("500 ml", "fënnefhonnert Milliliter"),
    ("1000ml", "dausend Milliliter"),
    ("Eng Fläsch vu 750ml", "Eng Fläsch vu siwenhonnertfofzeg Milliliter"),
    ("1gr", "ee Gramm"),
    ("50 gr", "fofzeg Gramm"),
    ("100gr", "honnert Gramm"),
    ("500 gr", "fënnefhonnert Gramm"),
    ("1000gr", "eendausend Gramm"),
    ("D'Paquet weit 500gr", "D'Paquet weit fënnefhonnert Gramm"),
    ("10%", "zéng Prozent"),
    ("25 %", "fënnefanzwanzeg Prozent"),
    ("50%", "fofzeg Prozent"),
    ("100 %", "eenhonnert Prozent"),
    ("Eng Erhéijung vun 10%", "Eng Erhéijung vun zéng Prozent"),
    ("de 4. Juni", "de véierte Juni"),
    ("den 1. Juni", "den éischte Juni"),
    ("den 2. Juni", "den zweete Juni"),
    ("den 3. Juni", "den drëtte Juni"),
    ("de 4. Juni", "de véierte Juni"),
    ("de 5. Juni", "de fënnefte Juni"),
    ("de 6. Juni", "de sechste Juni"),
    ("de 7. Juni", "de siwente Juni"),
])
def test_units(input_text, expected):
    normalizer = TextNormalizer()
    assert normalizer.normalize_text(input_text) == expected

# --- Mixed Examples ---
@pytest.mark.parametrize("input_text,expected", [
    ("1970er: 90° an 500ml Waasser mat 50gr Miel an 25% Zocker", "nonzénghonnertsiwwenzeger: nonzeg Grad an fënnefhonnert Milliliter Waasser mat fofzeg Gramm Miel an fënnefanzwanzeg Prozent Zocker"),
    ("2000er: Eng Fläsch vun 750ml an 1kg Miel", "zweedausender: Eng Fläsch vun siwenhonnertfofzeg Milliliter an ee Kilogramm Miel"),
    ("Am 1985er Wanter waren et -10°", "Am nonzénghonnertfënnefanachtzeger Wanter waren et minus zéng Grad"),
])
def test_mixed_examples(input_text, expected):
    normalizer = TextNormalizer()
    assert normalizer.normalize_text(input_text) == expected

# --- Edge Cases: Negative Temperatures, Large Numbers, Currency, Ordinals ---
def test_negative_temperatures():
    lb = Num2Word_LB()
    assert lb.to_unit("-1°") == "minus ee Grad"
    assert lb.to_unit("-10°") == "minus zéng Grad"

def test_large_numbers():
    lb = Num2Word_LB()
    assert "dausend" in lb.to_cardinal(1000)
    assert "eng Millioun" in lb.to_cardinal(1000000)
    assert "eng Milliard" in lb.to_cardinal(1000000000)
    assert "zwee Milliounen" in lb.to_cardinal(2000000)

def test_currency():
    lb = Num2Word_LB()
    assert "een Euro" in lb.to_currency(1, currency="EUR")
    assert "zwee Euro" in lb.to_currency(2, currency="EUR")
    assert "een Euro an een Cent" in lb.to_currency(1.01, currency="EUR")
    assert "zwee Euro a fofzeg Cent" in lb.to_currency(2.50, currency="EUR")
    assert "een Cent" in lb.to_currency(0.01, currency="EUR")
    assert "een Dollar" in lb.to_currency(1, currency="USD")
    assert "zwee Dollar a fënnefanzwanzeg Cent" in lb.to_currency(2.25, currency="USD")
    assert "ee Pond" in lb.to_currency(1, currency="GBP")
    assert "ee Yuan" in lb.to_currency(1, currency="CNY")
    assert "eng Mark" in lb.to_currency(1, currency="DEM")

def test_ordinals():
    lb = Num2Word_LB()
    assert lb.to_ordinal(100) == "eenhonnertsten"
    assert lb.to_ordinal(101) == "eenhonnertéischten"
    assert lb.to_ordinal(102) == "eenhonnertzweeten"
    assert lb.to_ordinal(110) == "eenhonnertzéngten"
    assert lb.to_ordinal(200) == "zweehonnertsten"
    assert lb.to_ordinal(1000) == "eendausendsten" 