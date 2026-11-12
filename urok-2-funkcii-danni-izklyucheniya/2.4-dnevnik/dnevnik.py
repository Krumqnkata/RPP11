"""dnevnik.py — среден успех и класация от речник с оценки.

Задача 2.4. Данните имат вида:

    {"име": {"предмет": [оценки], ...}, ...}

Нито една функция не бива да гърми при ученик без оценки
или при празен речник. Функциите връщат резултат и не печатат.
"""

STUDENTS = {
    "Ани":    {"математика": [6, 5, 6], "български": [5, 6], "история": [6]},
    "Борис":  {"математика": [3, 2, 4], "български": [3], "история": [4, 3]},
    "Вера":   {"математика": [5, 5], "български": [6, 6], "история": []},
    "Георги": {},
    "Диана":  {"математика": [2, 3], "български": [3, 4], "история": [3]},
}


def subject_average(student: dict, subject: str):
    """Среден успех по предмет. None, ако предметът липсва или няма оценки."""
    grades = student.get(subject)
    if not grades:
        return None
    return sum(grades) / len(grades)


def subject_averages(student: dict) -> dict:
    """Речник {предмет: среден успех} само за предметите с поне една оценка."""
    averages = {}
    for subject in student:
        average = subject_average(student, subject)
        if average is not None:
            averages[subject] = average
    return averages


def overall_average(student: dict):
    """Общ успех: средно аритметично на средните успехи по предмети.

    Предмети без оценки не участват. None, ако ученикът няма нито една оценка.
    """
    averages = subject_averages(student)
    if not averages:
        return None
    return sum(averages.values()) / len(averages)


def weakest_subject(student: dict):
    """Предметът с най-нисък среден успех. None, ако няма оценки.

    При равенство — първият по азбучен ред.
    """
    averages = subject_averages(student)
    if not averages:
        return None
    return min(averages, key=lambda subject: (averages[subject], subject))


def class_ranking(students: dict) -> list:
    """Списък от (име, общ успех), подреден от най-високия към най-ниския.

    Учениците без оценки са накрая (с успех None), подредени по азбучен ред.
    При равен успех — по азбучен ред на името.
    """
    with_grades, without_grades = [], []
    for name, student in students.items():
        average = overall_average(student)
        if average is None:
            without_grades.append((name, None))
        else:
            with_grades.append((name, average))
    with_grades.sort(key=lambda pair: (-pair[1], pair[0]))
    without_grades.sort()
    return with_grades + without_grades


def at_risk(students: dict, threshold: float = 3.50) -> list:
    """Имената (по азбучен ред) на учениците с общ успех под threshold.

    Ученици без оценки не се включват — за тях няма данни.
    """
    names = []
    for name, student in students.items():
        average = overall_average(student)
        if average is not None and average < threshold:
            names.append(name)
    return sorted(names)


if __name__ == "__main__":
    ani, vera, georgi = STUDENTS["Ани"], STUDENTS["Вера"], STUDENTS["Георги"]

    # subject_average
    assert subject_average(ani, "история") == 6
    assert subject_average(georgi, "история") is None      # ученик без предмети
    assert subject_average(vera, "история") is None        # предмет без оценки
    assert subject_average(ani, "химия") is None           # липсващ предмет

    # overall_average: средно на средните, а не на всички оценки
    assert abs(overall_average(ani) - (17 / 3 + 5.5 + 6) / 3) < 1e-9
    assert overall_average(vera) == 5.5                    # историята не участва
    assert overall_average(georgi) is None

    # weakest_subject
    assert weakest_subject(STUDENTS["Борис"]) == "български"   # равенство -> азбучен ред
    assert weakest_subject(georgi) is None

    # class_ranking
    ranking = class_ranking(STUDENTS)
    assert [name for name, _ in ranking] == ["Ани", "Вера", "Борис", "Диана", "Георги"]
    assert ranking[-1] == ("Георги", None)
    assert class_ranking({}) == []

    # at_risk
    assert at_risk(STUDENTS) == ["Борис", "Диана"]
    assert at_risk(STUDENTS, threshold=3.0) == []          # точно на прага не е в риск
    assert at_risk({}) == []

    print("Всички 15 проверки минаха.")
