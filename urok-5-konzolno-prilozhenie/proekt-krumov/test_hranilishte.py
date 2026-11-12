"""Проверки за hranilishte.py: зареждане и запис на задачите.

Пускане (от папката на проекта):  python -m pytest -v
Всяка проверка работи във временна папка (tmp_path), а не в data/.
"""
import hranilishte

TASKS = [
    {"tekst": "Домашно по математика", "gotova": False, "data": "2026-11-10"},
    {"tekst": "Купи тетрадка", "gotova": True, "data": "2026-11-11"},
]


def test_lipsvasht_fail_e_prazen_spisak(tmp_path):
    assert hranilishte.load_tasks(tmp_path / "nyama.txt") == ([], [])


def test_zapis_i_zarezhdane(tmp_path):
    path = tmp_path / "zadachi.txt"
    hranilishte.save_tasks(path, TASKS)
    assert hranilishte.load_tasks(path) == (TASKS, [])


def test_failat_e_v_utf8(tmp_path):
    path = tmp_path / "zadachi.txt"
    hranilishte.save_tasks(path, TASKS)
    text = path.read_bytes().decode("utf-8")      # гърми, ако не е UTF-8
    assert text.splitlines() == ["Домашно по математика | 0 | 2026-11-10",
                                 "Купи тетрадка | 1 | 2026-11-11"]


def test_zapisat_prezapisva_a_ne_dobavya(tmp_path):
    path = tmp_path / "zadachi.txt"
    hranilishte.save_tasks(path, TASKS)
    hranilishte.save_tasks(path, TASKS[:1])
    assert hranilishte.load_tasks(path) == (TASKS[:1], [])


def test_zapis_v_papka_koyato_oshte_ya_nyama(tmp_path):
    path = tmp_path / "data" / "zadachi.txt"
    hranilishte.save_tasks(path, TASKS)
    assert hranilishte.load_tasks(path) == (TASKS, [])


def test_povreden_fail_ne_spira_zarezhdaneto(tmp_path):
    path = tmp_path / "zadachi.txt"
    path.write_text("Първа | 0 | 2026-11-10\n"
                    "само текст без полета\n"
                    "\n"
                    "Втора | може би | 2026-11-11\n"
                    "Трета | 1 | 2026-11-12\n", encoding="utf-8")
    tasks, bad_lines = hranilishte.load_tasks(path)
    assert [task["tekst"] for task in tasks] == ["Първа", "Трета"]
    assert bad_lines == ["само текст без полета", "Втора | може би | 2026-11-11"]


def test_povredenite_redove_se_pazyat_otdelno(tmp_path):
    path = tmp_path / "zadachi_povredeni.txt"
    hranilishte.keep_bad_lines(path, ["лош ред 1"])
    hranilishte.keep_bad_lines(path, ["лош ред 2"])
    assert path.read_text(encoding="utf-8").splitlines() == ["лош ред 1", "лош ред 2"]
