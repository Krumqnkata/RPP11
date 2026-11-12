STUDENTS = {
    "Ани": [6, 5, 6, 4],
    "Борис": [3, 4, 3],
    "Валентин": [5, 6, 6, 5],
    "Вера": [5, 5, 6, 6, 5],
    "Георги": [],
    "Диана": [6, 6, 6],
}

EXCELLENT_FROM = 5.50


def average(grades):
    """Средно аритметично на оценките. None, ако няма нито една оценка."""
    if not grades:
        return None
    total = 0
    for g in grades:
        total += g
    return total / len(grades)


def is_excellent(avg):
    """True, ако успехът е отличен (от 5.50 нагоре). Без оценки — False."""
    return avg is not None and avg >= EXCELLENT_FROM


def ranking(students):
    """Списък от (име, успех) от най-високия успех към най-ниския.

    Учениците без оценки са накрая, с успех None.
    """
    result = []
    no_grades = []
    for name in students:
        avg = average(students[name])
        if avg is None:
            no_grades.append((name, None))
        else:
            result.append((name, avg))
    result.sort(key=lambda pair: pair[1], reverse=True)
    return result + no_grades


def print_report(students):
    """Отпечатва класацията, средния успех на класа и броя на отличниците."""
    print("КЛАСАЦИЯ")
    position = 0
    excellent_count = 0
    for name, avg in ranking(students):
        position += 1
        if avg is None:
            print(f"{position}. {name:10s} няма оценки")
            continue
        mark = ""
        if is_excellent(avg):
            mark = " *"
            excellent_count += 1
        print(f"{position}. {name:10s} {avg:.2f}{mark}")
    all_grades = []
    for name in students:
        all_grades += students[name]
    class_average = average(all_grades)
    if class_average is None:
        print("Среден успех на класа: няма оценки")
    else:
        print(f"Среден успех на класа: {class_average:.2f}")
    print(f"Брой отличници: {excellent_count}")


if __name__ == "__main__":
    print_report(STUDENTS)
    print(f"Най-добър ученик: {ranking(STUDENTS)[0][0]}")
