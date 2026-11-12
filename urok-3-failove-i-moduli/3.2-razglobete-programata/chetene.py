"""chetene.py — всичко, свързано с диска: четене на данните и запис на отчета."""


def read_lines(path) -> list:
    """Чете текстов файл в UTF-8 и връща редовете му като списък от низове.

    Ако файлът липсва, FileNotFoundError не се прехваща тук —
    какво да се прави тогава, решава викащият.
    """
    with open(path, encoding="utf-8") as f:
        return f.readlines()


def save_lines(path, lines: list) -> None:
    """Записва редовете във файл в UTF-8, по един на ред."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
