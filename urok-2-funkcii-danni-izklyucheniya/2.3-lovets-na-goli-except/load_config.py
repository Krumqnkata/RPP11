"""load_config.py — чете настройки от вида ключ=число.

Задача 2.3: в старата версия на функцията имаше четири проблема.
Те са описани в otgovori.md, а тук е поправената версия.
"""
from pathlib import Path

HERE = Path(__file__).parent  # папката на този файл, откъдето и да го стартирате


def load_config(path) -> dict:
    """Чете файл с редове „ключ=число“ и връща речник {ключ: число}.

    Празните редове и редовете, започващи с #, се пропускат.
    При повреден ред вдига ValueError с номера на реда.
    Ако файлът липсва, FileNotFoundError не се прехваща тук —
    какво да се прави тогава, решава викащият код.
    """
    data = {}
    with open(path, encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, separator, value = line.partition("=")
            if not separator:
                raise ValueError(f"Ред {number}: липсва знак '=' в '{line}'")
            try:
                data[key.strip()] = int(value.strip())
            except ValueError:
                raise ValueError(
                    f"Ред {number}: стойността '{value.strip()}' не е цяло число"
                ) from None
    return data


if __name__ == "__main__":
    for name in ("nastroyki.txt", "nastroyki_povredeni.txt", "nyama_takav_fail.txt"):
        try:
            result = load_config(HERE / name)
        except FileNotFoundError:
            result = "ЛИПСВА ТАКЪВ ФАЙЛ"
        except ValueError as err:
            result = f"ПОВРЕДЕН ФАЙЛ — {err}"
        print(f"{name:28s} -> {result}")
