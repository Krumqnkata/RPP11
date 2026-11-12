"""Проверки за логиката в zadachi.py.

Пускане (от папката на проекта):  python -m pytest -v
"""
import pytest

import zadachi

DATE = "2026-11-12"


@pytest.fixture
def tasks():
    """Списък с три задачи, втората е изпълнена."""
    return [
        {"tekst": "Домашно по математика", "gotova": False, "data": "2026-11-10"},
        {"tekst": "Купи тетрадка", "gotova": True, "data": "2026-11-11"},
        {"tekst": "Проект по РПП", "gotova": False, "data": "2026-11-12"},
    ]


# ---------- add_task ----------

def test_add_task_dobavya_neizpalnena_zadacha():
    tasks = []
    task = zadachi.add_task(tasks, "  Прочети урока  ", DATE)
    assert task == {"tekst": "Прочети урока", "gotova": False, "data": DATE}
    assert tasks == [task]


@pytest.mark.parametrize("text", ["", "   ", "\t"])
def test_add_task_prazen_tekst(text):
    tasks = []
    with pytest.raises(zadachi.InvalidText):
        zadachi.add_task(tasks, text, DATE)
    assert tasks == []


def test_add_task_razdelitel_v_teksta():
    with pytest.raises(zadachi.InvalidText):
        zadachi.add_task([], "мляко | хляб", DATE)


# ---------- task_index: капаните от картата ----------

def test_task_index_validen_nomer(tasks):
    assert zadachi.task_index(tasks, "1") == 0
    assert zadachi.task_index(tasks, " 3 ") == 2


@pytest.mark.parametrize("entered", ["7", "0", "-1", "4"])
def test_task_index_nomer_izvan_spisaka(tasks, entered):
    with pytest.raises(zadachi.InvalidNumber) as info:
        zadachi.task_index(tasks, entered)
    assert info.value.count == 3


@pytest.mark.parametrize("entered", ["две", "", "  ", "2.0", "1a"])
def test_task_index_ne_e_chislo(tasks, entered):
    with pytest.raises(zadachi.InvalidNumber):
        zadachi.task_index(tasks, entered)


def test_task_index_prazen_spisak():
    with pytest.raises(zadachi.InvalidNumber, match="празен"):
        zadachi.task_index([], "1")


def test_izklyucheniyata_nasledyavat_taskerror():
    assert issubclass(zadachi.InvalidNumber, zadachi.TaskError)
    assert issubclass(zadachi.InvalidText, zadachi.TaskError)


# ---------- mark_done и delete_task ----------

def test_mark_done(tasks):
    task = zadachi.mark_done(tasks, "1")
    assert task["gotova"] is True
    assert tasks[0]["gotova"] is True


def test_mark_done_nevaliden_nomer_ne_promenya_nishto(tasks):
    with pytest.raises(zadachi.InvalidNumber):
        zadachi.mark_done(tasks, "7")
    assert [task["gotova"] for task in tasks] == [False, True, False]


def test_delete_task(tasks):
    deleted = zadachi.delete_task(tasks, "2")
    assert deleted["tekst"] == "Купи тетрадка"
    assert [task["tekst"] for task in tasks] == ["Домашно по математика", "Проект по РПП"]


def test_delete_task_nevaliden_nomer_ne_iztriva_nishto(tasks):
    with pytest.raises(zadachi.InvalidNumber):
        zadachi.delete_task(tasks, "буква")
    assert len(tasks) == 3


# ---------- summary и форматиране ----------

def test_summary(tasks):
    assert zadachi.summary(tasks) == {"obshto": 3, "gotovi": 1, "ostavat": 2}
    assert zadachi.summary([]) == {"obshto": 0, "gotovi": 0, "ostavat": 0}


def test_format_tasks(tasks):
    lines = zadachi.format_tasks(tasks)
    assert lines[0] == " 1. [ ] Домашно по математика  (добавена на 10.11.2026)"
    assert lines[1] == " 2. [x] Купи тетрадка  (добавена на 11.11.2026)"
    assert zadachi.format_tasks([]) == []


# ---------- редове на файла ----------

def test_to_line_i_from_line_sa_obratni(tasks):
    for task in tasks:
        assert zadachi.from_line(zadachi.to_line(task)) == task


@pytest.mark.parametrize("line", [
    "Само текст",                          # 1 поле
    "Текст | 0",                           # 2 полета
    "Текст | 0 | 2026-11-12 | още",        # 4 полета
    " | 0 | 2026-11-12",                   # празен текст
    "Текст | да | 2026-11-12",             # състоянието не е 0 или 1
    "Текст | 0 | вчера",                   # датата не е дата
    "Текст | 0 | 2026-13-45",              # невъзможна дата
])
def test_from_line_povreden_red(line):
    assert zadachi.from_line(line) is None


def test_parse_lines_propuska_povredenite_i_gi_vrashta():
    lines = ["Първа | 0 | 2026-11-10\n", "\n", "повреден ред\n", "Втора | 1 | 2026-11-11\n"]
    tasks, bad_lines = zadachi.parse_lines(lines)
    assert [task["tekst"] for task in tasks] == ["Първа", "Втора"]
    assert bad_lines == ["повреден ред"]


def test_funktsiite_ne_pechatat(tasks, capsys):
    zadachi.add_task(tasks, "Нова", DATE)
    zadachi.mark_done(tasks, "1")
    zadachi.delete_task(tasks, "1")
    zadachi.format_tasks(tasks)
    zadachi.summary(tasks)
    assert capsys.readouterr().out == ""
