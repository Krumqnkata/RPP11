"""detektiv.py — в какво кодиране е записан файлът?

Задача 3.1. Четирите файла tekst_a.txt … tekst_d.txt съдържат един
и същ текст, но са записани в различни кодирания.
"""
from pathlib import Path

try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False

HERE = Path(__file__).parent
FILES = ["tekst_a.txt", "tekst_b.txt", "tekst_c.txt", "tekst_d.txt"]
ENCODINGS = ["utf-8", "cp1251", "utf-16", "latin-1"]

# Знаци, които почти никога не се срещат в български текст,
# но са типични за mojibake. Допълнете списъка, ако е нужно.
# Добавен е нулевият знак \x00: появява се, когато UTF-16 файл
# се прочете с еднобайтово кодиране (вижте коментара в края).
SUSPICIOUS = "ÃÐÑñÿÇäðàâåé\x00"


def preview(path, encoding: str, n: int = 40) -> str:
    """Първите n символа от файла, прочетен с даденото кодиране.

    Ако файлът не може да се прочете с това кодиране,
    UnicodeDecodeError не се прехваща тук — нека реши викащият.
    """
    with open(path, encoding=encoding) as f:
        return f.read(n)


def read_text(path, encoding: str) -> str:
    """Целият текст на файла, прочетен с даденото кодиране."""
    with open(path, encoding=encoding) as f:
        return f.read()


def has_bulgarian_letters(text: str) -> bool:
    """True, ако в текста има поне една буква от българската азбука."""
    return any("а" <= char.lower() <= "я" for char in text)


def has_suspicious_chars(text: str) -> bool:
    """True, ако в текста има знак от SUSPICIOUS."""
    return any(char in SUSPICIOUS for char in text)


def guess_encoding(path):
    """Името на първото кодиране от ENCODINGS, при което текстът
    съдържа български букви и няма знаци от SUSPICIOUS.
    None, ако нито едно не пасва.
    """
    for encoding in ENCODINGS:
        try:
            text = read_text(path, encoding)
        except UnicodeError:
            # UnicodeDecodeError е негов наследник. Нужен е родителят, защото
            # utf-16 без BOM вдига направо UnicodeError, а не UnicodeDecodeError.
            continue
        if has_bulgarian_letters(text) and not has_suspicious_chars(text):
            return encoding
    return None


def chardet_guess(path) -> tuple:
    """Догадката на пакета chardet: (кодиране, увереност от 0 до 1).

    chardet работи с байтове, затова файлът се отваря в двоичен режим
    ("rb") — там няма кодиране, което да се указва.
    """
    with open(path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"], result["confidence"]


def main() -> None:
    """Показва как изглежда всеки файл в четирите кодирания и догадката за него."""
    for name in FILES:
        print(f"\n=== {name} ===")
        for enc in ENCODINGS:
            try:
                # repr показва и невидимите знаци (\n, \x00, ﻿)
                print(f"  {enc:8s} {preview(HERE / name, enc)!r}")
            except UnicodeDecodeError as err:
                print(f"  {enc:8s} не става: {err.reason}")
            except UnicodeError as err:     # utf-16 без BOM в началото
                print(f"  {enc:8s} не става: {err}")
        print(f"  ДОГАДКА: {guess_encoding(HERE / name)}")
        if HAS_CHARDET:
            encoding, confidence = chardet_guess(HERE / name)
            print(f"  CHARDET: {encoding} (увереност {confidence:.2f})")
    if not HAS_CHARDET:
        print("\nПакетът 'chardet' не е инсталиран — сравнението е пропуснато.")
        print("Направи:  python -m pip install -r requirements.txt  (в корена)")


if __name__ == "__main__":
    main()

# СТЪПКА 4: кога методът ви би сгрешил? Отговорете тук в коментар.
#
# Върху четирите файла методът познава: a -> cp1251, b -> utf-8,
# c -> utf-16, d -> utf-8. Но той не „разбира“ текста, а само проверява
# дали има кирилски букви и дали няма знак от един къс списък. Затова
# греши в следните случаи:
#
# 1. Файл в друго кирилско кодиране. „Здравей, свят“ в KOI8-R, прочетено
#    като cp1251, става „ъДТБЧЕК, УЧСФ“ — пак само кирилски букви, макар и
#    грешните. При MIK/cp866 се получават кирилски букви и знаци като ‡ ¤ ©,
#    които ги няма в SUSPICIOUS. И в двата случая методът връща "cp1251",
#    въпреки че текстът е безсмислица: проверявам азбуката, а не думите.
#
# 2. UTF-16 файл, прочетен като cp1251. Първите два байта (BOM: FF FE)
#    се превръщат в „яю“ — български букви! Без \x00 в SUSPICIOUS методът
#    връщаше "cp1251" за tekst_c.txt. Нулевият знак ни спасява само защото
#    в текста има интервали, цифри и препинателни знаци (при тях вторият
#    байт е 00). UTF-16 текст само от кирилски букви би минал за cp1251.
#
# 3. tekst_d.txt е UTF-8 с BOM. Методът казва "utf-8" и текстът се чете,
#    но първият му символ е невидимият ﻿. Точният отговор е
#    "utf-8-sig", а това кодиране изобщо го няма в списъка ENCODINGS.
#
# 4. Редът в ENCODINGS решава: връща се първото, което пасва, а не
#    най-доброто. Ако cp1251 беше преди utf-8, резултатите щяха да са други.
#
# 5. latin-1 никога не гърми (всеки байт е валиден знак), но и никога не
#    дава български букви, така че методът никога няма да го върне.
#    За истински файл на френски или немски отговорът ще е None.
#
# 6. Текст без нито една българска буква (само цифри или английски) дава
#    None, въпреки че се чете правилно. А български текст с една чужда
#    дума като „café“ или „España“ се отхвърля заради é и ñ в SUSPICIOUS.
#
# РАЗШИРЕНИЕ: сравнение с пакета chardet (версия 7.7.0)
#
#   файл          моята догадка    chardet (увереност)
#   tekst_a.txt   cp1251           Windows-1251 (0.61)
#   tekst_b.txt   utf-8            utf-8        (0.99)
#   tekst_c.txt   utf-16           UTF-16       (1.00)
#   tekst_d.txt   utf-8            UTF-8-SIG    (1.00)
#
# За a, b и c двете догадки съвпадат (Windows-1251 е другото име на cp1251).
# Разликата е при tekst_d.txt: chardet гледа първите байтове, вижда BOM
# (EF BB BF) и казва UTF-8-SIG, а моят метод изобщо не познава това
# кодиране и оставя ﻿ в началото на текста.
#
# Другата разлика е в подхода. Моят метод отговаря с „да“ или „не“ и връща
# първото кодиране, което мине проверката. chardet работи с байтовете, а не
# с прочетения текст: сравнява колко често се срещат байтовете и двойките
# букви с типичното за всеки език и връща най-вероятното кодиране заедно с
# увереност. Затова при BOM е сигурен на 1.00, а при cp1251 — само на 0.61:
# еднобайтовите кирилски кодирания си приличат и той честно казва, че не е
# сигурен. Моят метод в същата ситуация (точка 1 по-горе) греши, без да
# подозира.
