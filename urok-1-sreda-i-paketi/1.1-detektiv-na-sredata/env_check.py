"""env_check.py — „Кой Python работи в момента?“

Изпълнете програмата два пъти: веднъж с глобалния Python и веднъж
от активирана виртуална среда. Сравнете реда „Текущ префикс“.
"""
import importlib.metadata
import os
import platform
import site
import sys


def in_virtualenv() -> bool:
    """Връща True, ако програмата се изпълнява във виртуална среда."""
    return sys.prefix != sys.base_prefix


def site_packages_dirs() -> list:
    """Връща пълните пътища до папките, в които живеят инсталираните пакети."""
    return site.getsitepackages()


def installed_packages_count() -> int:
    """Връща броя на пакетите, инсталирани за този Python."""
    names = {dist.metadata["Name"] for dist in importlib.metadata.distributions()}
    return len(names)


def report() -> None:
    """Отпечатва доклада за средата."""
    print("=" * 52)
    print("ДОКЛАД ЗА СРЕДАТА")
    print("=" * 52)
    print(f"Версия на Python : {platform.python_version()}")
    print(f"Изпълним файл    : {sys.executable}")
    print(f"Базов префикс    : {sys.base_prefix}")
    print(f"Текущ префикс    : {sys.prefix}")
    print(f"Работна папка    : {os.getcwd()}")
    for folder in site_packages_dirs():
        print(f"Папка с пакети   : {folder}")
    print(f"Брой пакети      : {installed_packages_count()}")
    print("-" * 52)
    if in_virtualenv():
        print("СТАТУС: РАБОТИШ ВЪВ ВИРТУАЛНА СРЕДА.")
    else:
        print("СТАТУС: ГЛОБАЛЕН PYTHON — внимавай какво инсталираш!")
        print("ВНИМАНИЕ: НЕ СИ ВЪВ ВИРТУАЛНА СРЕДА! АКТИВИРАЙ .venv ПРЕДИ pip install.")
    print("=" * 52)


if __name__ == "__main__":
    report()
