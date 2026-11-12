"""zadachi.py — чистата логика на списъка със задачи.

Функциите тук само приемат и връщат данни: не четат от клавиатурата,
не печатат и не докосват диска. Затова се проверяват без нито един файл.

Една задача е речник:

    {"tekst": "Домашно по математика", "gotova": False, "data": "2026-11-12"}

а списъкът със задачи е списък от такива речници.
"""
import datetime

SEPARATOR = "|"
FIELDS_PER_LINE = 3
DONE, NOT_DONE = "1", "0"


class TaskError(Exception):
    """Базово изключение на приложението — всички останали наследяват него."""


class InvalidText(TaskError):
    """Текстът на задачата е празен или съдържа разделителя."""


class InvalidNumber(TaskError):
    """Въведеното не е номер на задача от списъка."""

    def __init__(self, entered, count):
        if count == 0:
            hint = "списъкът е празен"
        else:
            hint = f"въведете число от 1 до {count}"
        super().__init__(f"Няма задача с номер '{entered}' — {hint}.")
        self.entered, self.count = entered, count


def clean_text(text: str) -> str:
    """Връща текста без интервалите в краищата.

    Вдига InvalidText, ако текстът е празен или съдържа знака |,
    който е разделителят във файла.
    """
    text = text.strip()
    if not text:
        raise InvalidText("Текстът на задачата не може да е празен.")
    if SEPARATOR in text:
        raise InvalidText(f"Текстът не може да съдържа знака '{SEPARATOR}'.")
    return text


def add_task(tasks: list, text: str, date: str) -> dict:
    """Добавя неизпълнена задача с дата date (ГГГГ-ММ-ДД). Връща новата задача."""
    task = {"tekst": clean_text(text), "gotova": False, "data": date}
    tasks.append(task)
    return task


def task_index(tasks: list, entered: str) -> int:
    """Превръща въведения от потребителя номер (от 1 нагоре) в индекс в списъка.

    Вдига InvalidNumber, ако въведеното не е цяло число
    или в списъка няма задача с такъв номер.
    """
    try:
        number = int(entered.strip())
    except ValueError:
        raise InvalidNumber(entered.strip(), len(tasks)) from None
    if not 1 <= number <= len(tasks):
        raise InvalidNumber(number, len(tasks))
    return number - 1


def mark_done(tasks: list, entered: str) -> dict:
    """Отбелязва задачата с въведения номер като изпълнена. Връща задачата."""
    task = tasks[task_index(tasks, entered)]
    task["gotova"] = True
    return task


def delete_task(tasks: list, entered: str) -> dict:
    """Изтрива задачата с въведения номер от списъка. Връща изтритата задача."""
    return tasks.pop(task_index(tasks, entered))


def summary(tasks: list) -> dict:
    """Връща речник с броя на всички, изпълнените и оставащите задачи."""
    done = sum(1 for task in tasks if task["gotova"])
    return {"obshto": len(tasks), "gotovi": done, "ostavat": len(tasks) - done}


def format_date(date: str) -> str:
    """Превръща датата от ГГГГ-ММ-ДД във вида ДД.ММ.ГГГГ."""
    return datetime.date.fromisoformat(date).strftime("%d.%m.%Y")


def format_task(number: int, task: dict) -> str:
    """Един ред от списъка: номер, отметка, текст и дата на добавяне."""
    mark = "x" if task["gotova"] else " "
    return f"{number:2d}. [{mark}] {task['tekst']}  (добавена на {format_date(task['data'])})"


def format_tasks(tasks: list) -> list:
    """Редовете на целия списък, номерирани от 1."""
    return [format_task(number, task) for number, task in enumerate(tasks, start=1)]


def to_line(task: dict) -> str:
    """Превръща задача в ред за файла: текст | 0 или 1 | дата."""
    state = DONE if task["gotova"] else NOT_DONE
    return f"{task['tekst']} {SEPARATOR} {state} {SEPARATOR} {task['data']}"


def from_line(line: str):
    """Превръща ред от файла в задача. None, ако редът е повреден.

    Повреден е ред с друг брой полета, с празен текст, със състояние,
    различно от 0 и 1, или с дата, която не е във вида ГГГГ-ММ-ДД.
    """
    parts = [part.strip() for part in line.split(SEPARATOR)]
    if len(parts) != FIELDS_PER_LINE:
        return None
    text, state, date = parts
    if not text or state not in (DONE, NOT_DONE):
        return None
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        return None
    return {"tekst": text, "gotova": state == DONE, "data": date}


def parse_lines(lines: list) -> tuple:
    """Превръща редовете на файла в (задачи, повредени редове).

    Празните редове се прескачат. Повредените не спират разбора,
    а се връщат отделно, за да не се изгубят мълчаливо.
    """
    tasks, bad_lines = [], []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        task = from_line(line)
        if task is None:
            bad_lines.append(line)
        else:
            tasks.append(task)
    return tasks, bad_lines
