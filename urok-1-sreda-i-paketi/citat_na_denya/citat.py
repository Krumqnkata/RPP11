"""citat.py — цитат на деня.

Цитатите се четат от data/citati.txt (един ред = „текст | автор“),
а не са записани в кода. Ако пакетът rich липсва, програмата работи
и без него, но казва какво трябва да се инсталира.
"""
import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

QUOTES_FILE = Path(__file__).parent / "data" / "citati.txt"


def parse_quote(line: str):
    """Разделя ред „текст | автор“ на (текст, автор). None, ако редът е повреден."""
    text, separator, author = line.rpartition("|")
    text, author = text.strip(), author.strip()
    if not separator or not text or not author:
        return None
    return text, author


def load_quotes(path) -> list:
    """Чете файла с цитати и връща списък от (текст, автор).

    Празните и повредените редове се пропускат. Ако файлът липсва,
    FileNotFoundError не се прехваща тук — решава викащият.
    """
    quotes = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            quote = parse_quote(line)
            if quote is not None:
                quotes.append(quote)
    return quotes


def quote_of_the_day(quotes: list, day: datetime.date) -> tuple:
    """Един и същ цитат за целия ден, различен за всеки ден."""
    return quotes[day.toordinal() % len(quotes)]


def show(text: str, author: str, day: datetime.date) -> None:
    """Отпечатва цитата — в рамка с rich или като обикновен текст."""
    if HAS_RICH:
        Console().print(Panel(f"[italic]{text}[/italic]\n\n[bold]— {author}[/bold]",
                              title=f"Цитат за {day:%d.%m.%Y}", border_style="cyan"))
    else:
        print("Пакетът 'rich' не е инсталиран в тази среда.")
        print("Направи:  python -m pip install -r requirements.txt")
        print(f"\n{text}\n— {author}")


def main() -> None:
    """Зарежда цитатите, избира днешния и го показва."""
    try:
        quotes = load_quotes(QUOTES_FILE)
    except FileNotFoundError:
        print(f"Липсва файлът с цитати: {QUOTES_FILE}")
        return
    if not quotes:
        print(f"Във файла {QUOTES_FILE.name} няма нито един валиден цитат.")
        return
    today = datetime.date.today()
    text, author = quote_of_the_day(quotes, today)
    show(text, author, today)


if __name__ == "__main__":
    main()
