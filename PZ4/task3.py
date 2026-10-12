# -*- coding: utf-8 -*-
"""
Задание 3. Система учёта студентов с валидацией и экспортом в CSV.
"""

import json
import os
import csv

STUDENTS_FILE = "students.json"
CSV_FILE = "students_export.csv"


def load_students():
    if not os.path.exists(STUDENTS_FILE):
        return []
    try:
        with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("Ошибка: students.json повреждён.")
            return []
        return data
    except json.JSONDecodeError:
        print("Ошибка: некорректный JSON в students.json.")
        return []
    except PermissionError:
        print("Ошибка: нет прав на чтение students.json.")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return []


def save_students(students):
    try:
        with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(students, f, ensure_ascii=False, indent=4)
        return True
    except PermissionError:
        print("Ошибка: нет прав на запись students.json.")
        return False
    except Exception as e:
        print(f"Неизвестная ошибка при сохранении: {e}")
        return False


def next_id(students):
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


def input_int(prompt, min_val=None, max_val=None):
    """Запрашивает целое число с проверкой диапазона."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Введите целое число.")
            continue
        if min_val is not None and value < min_val:
            print(f"Число должно быть не меньше {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Число должно быть не больше {max_val}.")
            continue
        return value


def input_grades():
    """Запрашивает оценки (2–5) через пробел."""
    while True:
        raw = input("Оценки через пробел (2–5): ").strip()
        if not raw:
            print("Введите хотя бы одну оценку.")
            continue
        try:
            grades = [int(x) for x in raw.split()]
        except ValueError:
            print("Оценки должны быть целыми числами.")
            continue
        if any(g < 2 or g > 5 for g in grades):
            print("Каждая оценка должна быть в диапазоне 2–5.")
            continue
        return grades


def add_student(students):
    name = input("Имя студента: ").strip()
    if not name:
        print("Имя не может быть пустым.")
        return
    age = input_int("Возраст (> 16): ", min_val=17)
    group = input("Группа: ").strip()
    if not group:
        print("Группа не может быть пустой.")
        return
    grades = input_grades()
    student = {
        "id": next_id(students),
        "name": name,
        "age": age,
        "group": group,
        "grades": grades,
    }
    students.append(student)
    if save_students(students):
        print(f"Студент #{student['id']} добавлен.")


def show_students(students):
    if not students:
        print("Список студентов пуст.")
        return
    print("\n--- Список студентов ---")
    for s in students:
        avg = sum(s["grades"]) / len(s["grades"]) if s["grades"] else 0
        print(f"#{s['id']} {s['name']} | возраст: {s['age']} | "
              f"группа: {s['group']} | оценки: {s['grades']} | средний: {avg:.2f}")
    print("-" * 30)


def find_student(students):
    query = input("Введите имя или группу для поиска: ").strip().lower()
    found = [s for s in students
             if query in s["name"].lower() or query in s["group"].lower()]
    if not found:
        print("Ничего не найдено.")
        return
    for s in found:
        avg = sum(s["grades"]) / len(s["grades"]) if s["grades"] else 0
        print(f"#{s['id']} {s['name']} | группа: {s['group']} | средний: {avg:.2f}")


def average_for_student(students):
    show_students(students)
    try:
        sid = int(input("Введите ID студента: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for s in students:
        if s["id"] == sid:
            if not s["grades"]:
                print("У студента нет оценок.")
                return
            avg = sum(s["grades"]) / len(s["grades"])
            print(f"Средний балл {s['name']}: {avg:.2f}")
            return
    print(f"Студент с ID {sid} не найден.")


def export_csv(students):
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Имя", "Возраст", "Группа", "Оценки", "Средний балл"])
            for s in students:
                avg = sum(s["grades"]) / len(s["grades"]) if s["grades"] else 0
                writer.writerow([
                    s["id"], s["name"], s["age"], s["group"],
                    " ".join(map(str, s["grades"])), f"{avg:.2f}"
                ])
        print(f"Экспорт в '{CSV_FILE}' выполнен.")
    except PermissionError:
        print("Ошибка: нет прав на запись CSV-файла.")
    except Exception as e:
        print(f"Ошибка экспорта: {e}")


def main():
    students = load_students()
    print(f"Загружено студентов: {len(students)}")

    while True:
        print("\nМеню:")
        print("1 — добавить студента")
        print("2 — показать всех")
        print("3 — найти по имени/группе")
        print("4 — средний балл студента")
        print("5 — экспорт в CSV")
        print("0 — выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            show_students(students)
        elif choice == "3":
            find_student(students)
        elif choice == "4":
            average_for_student(students)
        elif choice == "5":
            export_csv(students)
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()