# -*- coding: utf-8 -*-
"""
Задание 2. Менеджер задач с сохранением в tasks.json.

Каждая задача: {id, title, description, done}.
"""

import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    """Загружает задачи из файла. При ошибках возвращает []."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("Ошибка: файл tasks.json повреждён (ожидался список).")
            return []
        return data
    except json.JSONDecodeError:
        print("Ошибка: файл tasks.json содержит некорректный JSON.")
        return []
    except PermissionError:
        print("Ошибка: нет прав на чтение tasks.json.")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка при загрузке: {e}")
        return []


def save_tasks(tasks):
    """Сохраняет задачи в файл."""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
        return True
    except PermissionError:
        print("Ошибка: нет прав на запись tasks.json.")
        return False
    except Exception as e:
        print(f"Неизвестная ошибка при сохранении: {e}")
        return False


def next_id(tasks):
    """Генерирует следующий ID."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def add_task(tasks):
    title = input("Название задачи: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    description = input("Описание: ").strip()
    task = {
        "id": next_id(tasks),
        "title": title,
        "description": description,
        "done": False,
    }
    tasks.append(task)
    if save_tasks(tasks):
        print(f"Задача #{task['id']} добавлена.")


def show_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
        return
    print("\n Список задач")
    for t in tasks:
        status = "✔" if t["done"] else "✘"
        print(f"[{status}] #{t['id']} {t['title']} — {t['description']}")
    print("-" * 50)


def mark_done(tasks):
    show_tasks(tasks)
    try:
        tid = int(input("Введите ID выполненной задачи: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for t in tasks:
        if t["id"] == tid:
            t["done"] = True
            save_tasks(tasks)
            print(f"Задача #{tid} отмечена выполненной.")
            return
    print(f"Задача с ID {tid} не найдена.")


def delete_task(tasks):
    show_tasks(tasks)
    try:
        tid = int(input("Введите ID задачи для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for i, t in enumerate(tasks):
        if t["id"] == tid:
            confirm = input(f"Удалить задачу '{t['title']}'? (y/n): ").strip().lower()
            if confirm == "y":
                del tasks[i]
                save_tasks(tasks)
                print(f"Задача #{tid} удалена.")
            else:
                print("Удаление отменено.")
            return
    print(f"Задача с ID {tid} не найдена.")


def main():
    tasks = load_tasks()
    print(f"Загружено задач: {len(tasks)}")

    while True:
        print("\nМеню:")
        print("1 — добавить задачу")
        print("2 — показать все задачи")
        print("3 — отметить задачу выполненной")
        print("4 — удалить задачу")
        print("0 — выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()