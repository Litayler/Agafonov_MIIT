# -*- coding: utf-8 -*-
"""
Задание 1. Базовый файловый менеджер.

Позволяет:
- указать имя файла;
- создать его, если не существует;
- добавлять строки по одной;
- выводить содержимое после каждого добавления;
- обрабатывать ошибки доступа и кодировки.
"""

def read_file(filename):
    """Читает файл и возвращает список строк. При ошибках возвращает []."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []
    except PermissionError:
        print(f"Ошибка: нет прав доступа к файлу '{filename}'.")
        return []
    except UnicodeDecodeError:
        print(f"Ошибка: не удалось прочитать файл '{filename}' (проблема с кодировкой).")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка при чтении: {e}")
        return []


def append_line(filename, line):
    """Добавляет строку в файл. Возвращает True при успехе."""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return True
    except PermissionError:
        print(f"Ошибка: нет прав на запись в файл '{filename}'.")
        return False
    except UnicodeEncodeError:
        print("Ошибка: строка содержит символы, которые нельзя записать в utf-8.")
        return False
    except Exception as e:
        print(f"Неизвестная ошибка при записи: {e}")
        return False


def show_content(filename):
    """Выводит содержимое файла."""
    lines = read_file(filename)
    if not lines:
        print("(файл пуст или не существует)")
        return
    print(f"--- Содержимое '{filename}' ---")
    for i, line in enumerate(lines, 1):
        print(f"{i}: {line.rstrip()}")
    print("-" * 30)


def main():
    filename = input("Введите имя файла (например, notes.txt): ").strip()
    if not filename:
        print("Имя файла не может быть пустым.")
        return

    # Создаём файл, если нет
    try:
        with open(filename, "a", encoding="utf-8"):
            pass
        print(f"Файл '{filename}' готов к работе.")
    except PermissionError:
        print(f"Ошибка: нет прав на создание/открытие файла '{filename}'.")
        return
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    while True:
        print("\nМеню:")
        print("1 — добавить строку")
        print("2 — показать содержимое")
        print("0 — выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            line = input("Введите строку: ")
            if append_line(filename, line):
                show_content(filename)
        elif choice == "2":
            show_content(filename)
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()