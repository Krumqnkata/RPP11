"""hranilishte.py — всичко, свързано с диска: зареждане и запис на задачите.

Файлът е текстов, в UTF-8, по една задача на ред:

    текст | 0 или 1 | дата (ГГГГ-ММ-ДД)

Как един ред става задача и обратно, знае zadachi.py — тук само
се чете и се пише.
"""
import zadachi


def load_tasks(path) -> tuple:
    """Чете файла със задачите. Връща (задачи, повредени редове).

    Ако файлът липсва, списъкът е празен: връща ([], []).
    Това не е грешка — така изглежда първото стартиране.
    """
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [], []
    return zadachi.parse_lines(lines)


def save_tasks(path, tasks: list) -> None:
    """Записва всички задачи във файла, по една на ред (презаписва го)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(zadachi.to_line(task) + "\n")


def keep_bad_lines(path, bad_lines: list) -> None:
    """Добавя повредените редове в края на отделен файл.

    Файлът със задачите се презаписва при всяка промяна и повредените
    редове биха изчезнали от него. Тук се пазят, за да може човек
    да ги поправи на ръка.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for line in bad_lines:
            f.write(line + "\n")
