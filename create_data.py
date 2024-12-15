from sqlalchemy import create_engine, text
from configs.config_app_user import dbname, user, password, host, port
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

DATABASE_URL = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(DATABASE_URL)


def truncate_tables():
    """
    Удаляет данные из всех таблиц и сбрасывает автоинкременты.
    """
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users.Reviews"))
        connection.execute(text("DELETE FROM games.Games"))
        connection.execute(text("DELETE FROM games.Developers"))
        connection.execute(text("DELETE FROM games.Genres"))
        connection.execute(text("DELETE FROM auth.Users"))

        connection.execute(text("TRUNCATE TABLE users.Reviews RESTART IDENTITY CASCADE"))
        connection.execute(text("TRUNCATE TABLE games.Games RESTART IDENTITY CASCADE"))
        connection.execute(text("TRUNCATE TABLE games.Developers RESTART IDENTITY CASCADE"))
        connection.execute(text("TRUNCATE TABLE games.Genres RESTART IDENTITY CASCADE"))
        connection.execute(text("TRUNCATE TABLE auth.Users RESTART IDENTITY CASCADE"))
        print("All tables truncated and auto-increment values reset.")


def call_procedure(procedure_name, params):
    with engine.connect() as connection:
        connection.execute(text(f"CALL {procedure_name}(:{', :'.join(params.keys())})"), params)
        connection.commit()


def add_users():
    users = [
        {"p_username": "admin_user", "p_password": "admin_password", "p_role": "admin"},
        {"p_username": "regular_user", "p_password": "user_password", "p_role": "user"}
    ]
    for user in users:
        call_procedure("auth.add_user", user)
    print("Users added successfully!")


def add_developers():
    developers = [
        {"p_name": "CD Projekt Red", "p_country": "Poland"},
        {"p_name": "FromSoftware", "p_country": "Japan"},
        {"p_name": "Team Cherry", "p_country": "Australia"}
    ]
    for dev in developers:
        call_procedure("games.add_developer", dev)
    print("Developers added successfully!")


def add_genres():
    genres = [
        {"p_name": "RPG"},
        {"p_name": "Action"},
        {"p_name": "Metroidvania"}
    ]
    for genre in genres:
        call_procedure("games.add_genre", genre)
    print("Genres added successfully!")


def add_games():
    games = [
        {"p_title": "The Witcher 3", "p_description": "Fantasy RPG in an open world", "p_release_date": "2015-05-19",
         "p_developer_id": 1, "p_genre_id": 1, "p_average_rating": 9.5},
        {"p_title": "Elden Ring", "p_description": "Open-world action RPG", "p_release_date": "2022-02-25",
         "p_developer_id": 2, "p_genre_id": 1, "p_average_rating": 9.8},
        {"p_title": "Hollow Knight", "p_description": "Metroidvania platformer", "p_release_date": "2017-02-24",
         "p_developer_id": 3, "p_genre_id": 3, "p_average_rating": 9.4}
    ]
    for game in games:
        call_procedure("games.add_game", game)
    print("Games added successfully!")


def add_reviews():
    reviews = [
        {"p_game_id": 1, "p_user_id": 2, "p_rating": 10, "p_comment": "Amazing game!"},
        {"p_game_id": 2, "p_user_id": 1, "p_rating": 9, "p_comment": "Stunning visuals and gameplay."},
        {"p_game_id": 3, "p_user_id": 2, "p_rating": 9, "p_comment": "Incredible atmosphere."}
    ]
    for review in reviews:
        call_procedure("users.add_review", review)
    print("Reviews added successfully!")


def populate_database():
    truncate_tables()  # Удаляем все данные из таблиц
    # add_users()
    add_developers()
    add_genres()
    add_games()
    add_reviews()
    print("Database populated successfully!")


populate_database()
