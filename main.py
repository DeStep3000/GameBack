from sqlalchemy import create_engine, text
from configs.config_app_user import dbname, user, password, host, port


# 1. Создание таблиц
def create_tables():
    with engine.connect() as connection:
        connection.execute(text("CALL system.create_tables()"))


# 2. Удаление всех таблиц
def drop_tables():
    with engine.connect() as connection:
        connection.execute(text("CALL system.drop_all_tables()"))


# 3. Очистка таблиц
def clear_table(table_name):
    with engine.connect() as connection:
        connection.execute(text("CALL system.clear_table(:table_name)"), {"table_name": table_name})


# 4. Добавление игры
def add_game():
    title = input("Enter game title: ")
    description = input("Enter description: ")
    release_date = input("Enter release date (YYYY-MM-DD): ")
    developer_id = input("Enter developer ID: ")
    genre_id = input("Enter genre ID: ")
    average_rating = input("Enter average rating: ")

    with engine.connect() as connection:
        connection.execute(text("""
            CALL games.add_game(
                :p_title, :p_description, :p_release_date, 
                :p_developer_id, :p_genre_id, :p_average_rating
            )
        """), {
            "p_title": title,
            "p_description": description,
            "p_release_date": release_date,
            "p_developer_id": developer_id,
            "p_genre_id": genre_id,
            "p_average_rating": average_rating
        })


if __name__ == '__main__':
    DATABASE_URL = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(DATABASE_URL)

    # Работет ли эта хуйня
    with engine.connect() as conn:
        result = conn.execute(text('SELECT version();'))
        for row in result:
            print(f'PostgreSQL Version: {row[0]}')
