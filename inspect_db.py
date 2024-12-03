import sqlite3

# PATH db - Путь к вашей базе данных
DB_PATH = "C:\\Users\\All\\MyDjangoProjects\\MyFastAPIProjects\\notes.db"


# function for execute SQL-команд
def execute_sql(sql, parameters=None):
    try:
        # connection sqlite3 - Подключение к базе данных
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        print("Подключено.")

        # execute SQL-request - Выполнение SQL-запроса
        if parameters:
            cursor.execute(sql, parameters)
        else:
            cursor.execute(sql)

        # If this is a change request - Если это запрос изменения (INSERT/UPDATE/DELETE), record changes -фиксируем изменения
        if sql.strip().lower().startswith(("insert", "update", "delete", "create", "drop")):
            connection.commit()
            print("Изменения успешны.")

        # Если это SELECT-запрос, возвращаем результат
        if sql.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    except sqlite3.Error as e:
        print(f"Ошибка работы с базой данных: {e}")
    finally:
        # Closing connection - Закрытие подключения
        if connection:
            connection.close()
            print("Подключение закрыто.")


# Функция для массового добавления записей
def add_notes(notes):
    for note in notes:
        execute_sql(
            "INSERT OR IGNORE INTO notes (id, title, content) VALUES (?, ?, ?)",
            note
        )


# Проверка и создание таблицы, если её нет
def ensure_table_exists():
    execute_sql("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)


# execute
if __name__ == "__main__":
    # Убедимся, что таблица существует
    ensure_table_exists()

    # 1. Adding new records to a table - Добавление новых записей в таблицу
    print("\nДобавление новых записей:")
    execute_sql(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        ("Планы на день", "1. Выполнить утреннюю тренировку. 2. Написать отчёт по проекту.")
    )
    execute_sql(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        ("Изучение SQLite", "Изучить основные команды работы с SQLite: SELECT, INSERT, UPDATE, DELETE.")
    )

    # 2. Updating the entry - Обновление записи
    print("\nОбновление записи:")
    execute_sql(
        "UPDATE notes SET content = ? WHERE id = ?",
        ("Выполнить тренировку и обновить отчёт до обеда.", 1)
    )
    execute_sql(
        "UPDATE notes SET title = ?, content = ? WHERE id = ?",
        ("Изучение SQLite и FastAPI", "Добавить примеры работы с FastAPI в проект.", 2)
    )

    # 3. Deleting a record - Удаление записи
    print("\nУдаление записи:")
    execute_sql(
        "DELETE FROM notes WHERE id = ?",
        (13,14,15,16)  # ID записи для удаления
    )
    execute_sql(
        "DELETE FROM notes WHERE title = ?",
        ("Цели до конца года",)  # Удаление по названию
    )
    # Добавление недостающих записей
    missing_notes = [
        (1, "Утренние планы", "Сделать зарядку, приготовить завтрак, написать заметку."),
        (2, "Вечерние планы", "Посмотреть сериал, прочитать книгу, приготовить ужин."),
        (3, "Заметка о работе", "Закончить проект, подготовить отчёт, обсудить новые задачи.")
    ]
    for note in missing_notes:
        execute_sql(
            "INSERT OR IGNORE INTO notes (id, title, content) VALUES (?, ?, ?)",
            note
        )
    # 4. Adding multiple records - Добавление нескольких записей
    notes = [
        (4, "Посмотреть ролик о FastAPI", "Сегодня вечером посмотреть 'Python FastAPI Tutorial'."),
        (5, "План тренировок и массажа",
         "Понедельник: упражнения с роллом, вторник: массаж Ток-сен, среда: упражнения для шеи и рук, четверг: упражнения для спины и ног."),
        (6, "Рецепт пасты",
         "Ингредиенты: паста, томаты, базилик, чеснок. Приготовление: обжарить чеснок, добавить томаты, заправить пасту."),
        (7, "Цели до конца года",
         "1. Закончить проект. 2. Сдать экзамен по теме \"Разработка веб-приложений с использованием Python\". 3. Начать учить английский язык. 4. Минимизировать траты."),
        (8, "День рождения в соцсетях", "Поздравить друзей в Вайбере и Фэйсбуке. Найти красивую открытку."),
        (9, "Запись к врачу", "В пятницу записаться на прием к терапевту на 10.00."),
        (10, "Заменить процессор", "Найти обновленную версию процессора.")
    ]
    print("\nДобавление нескольких записей:")
    add_notes(notes)

    # 5. View all posts - Просмотр всех записей
    print("\nСписок всех заметок:")
    execute_sql("SELECT * FROM notes")

    # 6. Getting the table structure - Получение структуры таблицы
    print("\nСтруктура таблицы:")
    execute_sql("PRAGMA table_info(notes)")