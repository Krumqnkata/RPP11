"""main.py — Списък със задачи.

Пази списък със задачи в текстов файл: добавя, показва, отбелязва
като изпълнени и изтрива задачи.

Тук е само входът и изходът. Логиката е в zadachi.py,
а четенето и записът на файла — в hranilishte.py.
"""
import datetime
from pathlib import Path

import hranilishte
import zadachi

DATA_DIR = Path(__file__).parent / "data"
TASKS_FILE = DATA_DIR / "zadachi.txt"
BAD_LINES_FILE = DATA_DIR / "zadachi_povredeni.txt"

MENU = """
1. Добави задача
2. Покажи списъка
3. Отбележи задача като изпълнена
4. Изтрий задача
5. Изход"""
EXIT_CHOICE = "5"


def show_tasks(tasks: list) -> None:
    """Отпечатва номерирания списък и обобщението под него."""
    if not tasks:
        print("Списъкът е празен.")
        return
    for line in zadachi.format_tasks(tasks):
        print(line)
    counts = zadachi.summary(tasks)
    print(f"Общо: {counts['obshto']}, изпълнени: {counts['gotovi']}, "
          f"остават: {counts['ostavat']}")


def save(tasks: list) -> None:
    """Записва списъка във файла и казва, ако записът не е успял."""
    try:
        hranilishte.save_tasks(TASKS_FILE, tasks)
    except OSError as err:
        print(f"ВНИМАНИЕ: промяната не е записана във файла: {err}")


def load() -> list:
    """Зарежда задачите при стартиране и съобщава за повредените редове."""
    tasks, bad_lines = hranilishte.load_tasks(TASKS_FILE)
    print(f"Заредени задачи: {len(tasks)}")
    if bad_lines:
        hranilishte.keep_bad_lines(BAD_LINES_FILE, bad_lines)
        save(tasks)
        print(f"Пропуснати повредени редове: {len(bad_lines)} "
              f"(преместени са в {BAD_LINES_FILE.name})")
    return tasks


def add(tasks: list) -> bool:
    """Пита за текст и добавя задача. Връща True, ако списъкът е променен."""
    text = input("Текст на задачата: ")
    try:
        task = zadachi.add_task(tasks, text, datetime.date.today().isoformat())
    except zadachi.InvalidText as err:
        print(err)
        return False
    print(f"Добавена: {task['tekst']}")
    return True


def mark(tasks: list) -> bool:
    """Пита за номер и отбелязва задачата. Връща True, ако списъкът е променен."""
    show_tasks(tasks)
    if not tasks:
        return False
    try:
        task = zadachi.mark_done(tasks, input("Номер на изпълнената задача: "))
    except zadachi.InvalidNumber as err:
        print(err)
        return False
    print(f"Изпълнена: {task['tekst']}")
    return True


def delete(tasks: list) -> bool:
    """Пита за номер и изтрива задачата. Връща True, ако списъкът е променен."""
    show_tasks(tasks)
    if not tasks:
        return False
    try:
        task = zadachi.delete_task(tasks, input("Номер на задачата за изтриване: "))
    except zadachi.InvalidNumber as err:
        print(err)
        return False
    print(f"Изтрита: {task['tekst']}")
    return True


def show(tasks: list) -> bool:
    """Показва списъка. Нищо не променя, затова връща False."""
    show_tasks(tasks)
    return False


ACTIONS = {"1": add, "2": show, "3": mark, "4": delete}


def main() -> None:
    """Главният цикъл на програмата: само вход и изход."""
    print("СПИСЪК СЪС ЗАДАЧИ")
    try:
        tasks = load()
    except UnicodeDecodeError:
        # Ако продължим с празен списък, първият запис ще изтрие файла.
        print(f"Файлът {TASKS_FILE.name} не е в UTF-8 и не може да се прочете.")
        print("Поправете кодирането му или го преместете и стартирайте отново.")
        return

    while True:
        print(MENU)
        choice = input("Избор (1-5): ").strip()
        if choice == EXIT_CHOICE:
            print("Довиждане!")
            return
        action = ACTIONS.get(choice)
        if action is None:
            print(f"Няма опция '{choice}'. Въведете число от 1 до 5.")
            continue
        changed = action(tasks)
        if changed:
            save(tasks)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C или край на входа: всяка промяна вече е записана във файла.
        print("\nДовиждане!")
