"""sled.py — средният успех, поправен така, че да не гърми при неочакван вход.

Логиката (average, grade_name) само смята и връща. Входът и изходът са
в read_int, read_grades и main. При грешен вход програмата казва какво
не е наред и пита отново, вместо да спре или да смята с грешни числа.
"""
MIN_GRADE, MAX_GRADE = 2, 6
MAX_COUNT = 50

GRADE_NAMES = [            # (от успех, име) — от най-високия към най-ниския
    (5.50, "Отличен"),
    (4.50, "Много добър"),
    (3.50, "Добър"),
    (3.00, "Среден"),
]


def average(grades: list):
    """Средно аритметично на оценките. None, ако списъкът е празен."""
    if not grades:
        return None
    return sum(grades) / len(grades)


def grade_name(avg: float) -> str:
    """Словесната оценка за даден среден успех."""
    for lower_bound, name in GRADE_NAMES:
        if avg >= lower_bound:
            return name
    return "Слаб"


def parse_int(text: str, low: int, high: int) -> int:
    """Превръща текста в цяло число от low до high.

    Вдига ValueError с разбираемо съобщение, ако текстът е празен,
    не е цяло число или е извън границите.
    """
    text = text.strip()
    if not text:
        raise ValueError("Не сте въвели нищо.")
    try:
        number = int(text)
    except ValueError:
        raise ValueError(f"'{text}' не е цяло число.") from None
    if not low <= number <= high:
        raise ValueError(f"Числото трябва да е от {low} до {high}, а е {number}.")
    return number


def read_int(prompt: str, low: int, high: int) -> int:
    """Пита, докато потребителят въведе цяло число от low до high."""
    while True:
        try:
            return parse_int(input(prompt), low, high)
        except ValueError as err:
            print(f"  {err} Опитайте пак.")


def read_grades() -> list:
    """Пита колко са оценките и ги прочита една по една."""
    count = read_int("Колко оценки имаш? ", 1, MAX_COUNT)
    return [read_int(f"Оценка {i}: ", MIN_GRADE, MAX_GRADE)
            for i in range(1, count + 1)]


def main() -> None:
    """Чете оценките и отпечатва средния успех."""
    grades = read_grades()
    avg = average(grades)
    print(f"Среден успех: {avg:.2f}")
    print(grade_name(avg))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрекъснато — нищо не е изчислено.")
