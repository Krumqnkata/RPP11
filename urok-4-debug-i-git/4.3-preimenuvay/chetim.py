"""chetim.py — същата логика като nechetim.py, но с имена, които се четат.

Намира учениците, чийто среден успех е поне колкото зададения праг.
Ученици без оценки не участват.
"""


def average(grades):
    """Средно аритметично на оценките. None, ако няма нито една оценка."""
    if not grades:
        return None
    return sum(grades) / len(grades)


def students_with_average_at_least(grades_by_student, threshold):
    """Списък от (име, среден успех) за учениците с успех поне threshold."""
    selected = []
    for name, grades in grades_by_student.items():
        student_average = average(grades)
        if student_average is None:
            continue
        if student_average >= threshold:
            selected.append((name, student_average))
    return selected


if __name__ == "__main__":
    danni = {
        "Ани": [6, 5, 6, 4],
        "Борис": [3, 4, 3],
        "Валентин": [5, 6, 6, 5],
        "Георги": [],
        "Диана": [6, 6, 6],
    }
    print(students_with_average_at_least(danni, 5.0))
    print(students_with_average_at_least(danni, 5.5))
    print(students_with_average_at_least({}, 4.0))
