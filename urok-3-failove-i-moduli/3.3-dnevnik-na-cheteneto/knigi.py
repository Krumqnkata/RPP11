"""knigi.py — дневник на прочетените книги в текстов файл.

Задача 3.3. Един ред във файла е една книга:

    заглавие | автор | година на прочитане | оценка от 1 до 6

Правила: файлът се отваря само с with и само с явно кодиране;
повреден ред не спира програмата.
"""
from pathlib import Path

HERE = Path(__file__).parent
KNIGI = HERE / "knigi.txt"
OTCHET = HERE / "otchet.txt"

SEPARATOR = "|"
FIELDS_PER_LINE = 4
MIN_RATING, MAX_RATING = 1, 6


def valid_rating(rating: int) -> bool:
    """True, ако оценката е между 1 и 6 включително."""
    return MIN_RATING <= rating <= MAX_RATING


def ends_with_newline(path) -> bool:
    """True, ако файлът липсва, празен е или завършва с нов ред."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return True
    return text == "" or text.endswith("\n")


def add_book(path, title: str, author: str, year: int, rating: int) -> None:
    """Добавя ред в края на файла, без да презаписва старите.

    При оценка извън 1..6 вдига ValueError и не пише нищо.
    """
    if not valid_rating(rating):
        raise ValueError(f"Оценката трябва да е от {MIN_RATING} до {MAX_RATING}, "
                         f"а е {rating}")
    if SEPARATOR in title or SEPARATOR in author:
        raise ValueError(f"Заглавието и авторът не може да съдържат '{SEPARATOR}'")
    # Ако последният ред няма нов ред накрая, новата книга би се залепила за него.
    prefix = "" if ends_with_newline(path) else "\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{prefix}{title} | {author} | {year} | {rating}\n")


def parse_book(line: str):
    """Превръща един ред в речник за книга. None, ако редът е повреден."""
    parts = [part.strip() for part in line.split(SEPARATOR)]
    if len(parts) != FIELDS_PER_LINE:
        return None
    title, author, year, rating = parts
    try:
        year, rating = int(year), int(rating)
    except ValueError:
        return None
    if not valid_rating(rating):
        return None
    return {"zaglavie": title, "avtor": author, "godina": year, "otsenka": rating}


def load_books(path) -> tuple:
    """Чете файла. Връща (книги, брой_пропуснати_редове).

    Всяка книга е речник с ключове "zaglavie", "avtor",
    "godina" (int) и "otsenka" (int).
    Пропуска повредените редове: с друг брой полета, с година
    или оценка, която не е число, или с оценка извън 1..6.
    Ако файлът липсва, дневникът е празен: връща ([], 0).
    """
    books, skipped = [], 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue            # празният ред не е повреден
                book = parse_book(line)
                if book is None:
                    skipped += 1
                else:
                    books.append(book)
    except FileNotFoundError:
        return [], 0
    return books, skipped


def stats(books: list) -> dict:
    """Връща речник с ключове:

    "sredna_otsenka" — средната оценка (None при празен списък),
    "nay_dobra"      — заглавието с най-висока оценка
                       (при равенство — първото във файла; None при празен списък),
    "po_godini"      — речник {година: брой книги}.
    """
    if not books:
        return {"sredna_otsenka": None, "nay_dobra": None, "po_godini": {}}
    by_year = {}
    for book in books:
        by_year[book["godina"]] = by_year.get(book["godina"], 0) + 1
    best = max(books, key=lambda book: book["otsenka"])   # max връща първата най-висока
    return {
        "sredna_otsenka": sum(book["otsenka"] for book in books) / len(books),
        "nay_dobra": best["zaglavie"],
        "po_godini": by_year,
    }


def report_lines(books: list) -> list:
    """Редовете на отчета: обобщение, после книгите по години и по оценка."""
    summary = stats(books)
    lines = ["ДНЕВНИК НА ЧЕТЕНЕТО", f"Прочетени книги: {len(books)}"]
    if not books:
        return lines
    lines.append(f"Средна оценка: {summary['sredna_otsenka']:.2f}")
    lines.append(f"Най-добра книга: {summary['nay_dobra']}")
    for year in sorted(summary["po_godini"]):
        lines += ["", f"{year} г. — брой книги: {summary['po_godini'][year]}"]
        from_year = [book for book in books if book["godina"] == year]
        for book in sorted(from_year, key=lambda book: (-book["otsenka"], book["zaglavie"])):
            lines.append(f"  {book['otsenka']}  {book['zaglavie']} — {book['avtor']}")
    return lines


def export_report(path, books: list) -> None:
    """Записва подреден текстов отчет в UTF-8."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines(books)) + "\n")


if __name__ == "__main__":
    books, skipped = load_books(KNIGI)
    print(f"Заредени {len(books)} книги, пропуснати {skipped} повредени реда.")
    export_report(OTCHET, books)
    for line in report_lines(books):
        print(line)
    print(f"\nОтчетът е записан в {OTCHET.name}")
