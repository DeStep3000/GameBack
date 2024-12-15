from sqlalchemy import create_engine, text
from configs.config_app_user import dbname, user, password, host, port
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

DATABASE_URL = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(DATABASE_URL)


# Вызов процедуры через SQLAlchemy
def call_procedure(procedure_name, params):
    with engine.connect() as connection:
        connection.execute(
            text(f"CALL {procedure_name}(:{', :'.join(params.keys())})"), params
        )
        connection.commit()


def add_users():
    users = [
        {"p_username": "admin_user", "p_password": "admin_password", "p_role": "admin"},
        {"p_username": "regular_user", "p_password": "user_password", "p_role": "user"},
    ]
    for user in users:
        try:
            call_procedure("auth.add_user", user)
            print(f"User {user['p_username']} added successfully!")
        except Exception as e:
            print(f"Error adding user {user['p_username']}: {e}")


# Данные для заполнения
platforms = [
    {"p_name": "Windows"},
    {"p_name": "PlayStation 4"},
    {"p_name": "PlayStation 5"},
    {"p_name": "Xbox One"},
    {"p_name": "Xbox Series X/S"},
    {"p_name": "macOS"},
    {"p_name": "Linux"},
    {"p_name": "Nintendo Switch"},
    {"p_name": "PlayStation 3"},
    {"p_name": "Xbox 360"},
    {"p_name": "Android"},
]

developers = [
    {"p_name": "Riot Games", "p_country": "США"},
    {"p_name": "Valve", "p_country": "США"},
    {"p_name": "miHoYo Limited", "p_country": "Китай"},
    {"p_name": "Consumer Games Development Division 1", "p_country": "Япония"},
    {"p_name": "CD Projekt RED", "p_country": "Польша"},
    {"p_name": "FromSoftware", "p_country": "Япония"},
    {"p_name": "SCS Software", "p_country": "Чехия"},
    {"p_name": "Rockstar North", "p_country": "Великобритания"},
    {"p_name": "Mundfish", "p_country": "Россия"},
    {"p_name": "NetherRealm Studios", "p_country": "США"},
    {"p_name": "EA Vancouver", "p_country": "Канада"},
    {"p_name": "Facepunch Studios", "p_country": "Британия"},
    {"p_name": "Double Eleven", "p_country": "Британия"},
    {"p_name": "Kinetic Games", "p_country": "Британия"},
    {"p_name": "The Sims Studio", "p_country": "США"},
    {"p_name": "4A Games", "p_country": "Украина"},
]

genres = [
    {"p_name": "Геройский ШПЛ"},
    {"p_name": "MOBA"},
    {"p_name": "Тактический ШПЛ"},
    {"p_name": "Action/RPG"},
    {"p_name": "survival horror"},
    {"p_name": "Remake"},
    {"p_name": "симулятор"},
    {"p_name": "шутер от первого лица"},
    {"p_name": "action-adventure"},
    {"p_name": "футбольный симулятор"},
    {"p_name": "Файтинг"},
    {"p_name": "симулятор выживания"},
]

games = [{'p_title': 'Valorant',
          'p_description': 'Valorant — командный тактический шутер от первого лица. Игроки делятся на две команды по 5 человек и сражаются в различных режимах, где одна сторона атакует, а другая защищает. Игра сочетает в себе элементы тактики и стратегического планирования, предлагая уникальных персонажей (агентов), каждый из которых обладает своими способностями.',
          'p_release_date': '2020-06-02', 'p_developer_id': 1, 'p_genre_id': 1, 'p_average_rating': 9.0},
         {'p_title': 'Dota 2',
          'p_description': 'Dota 2 — многопользовательская командная компьютерная игра. В ней две команды по пять игроков сражаются на карте, стремясь уничтожить особый объект соперника — трон, и в то же время защитить от уничтожения собственный. Каждый игрок управляет героем с уникальными способностями и ролями, требующими стратегического подхода и командного взаимодействия.',
          'p_release_date': '2013-07-09', 'p_developer_id': 2, 'p_genre_id': 2, 'p_average_rating': 9.2},
         {'p_title': 'Counter-Strike 2',
          'p_description': 'Counter-Strike 2 — тактический шутер от первого лица. Игроки делятся на команды террористов и контртеррористов, выполняя задачи, такие как установка или обезвреживание бомбы.',
          'p_release_date': '2023-09-27', 'p_developer_id': 2, 'p_genre_id': 3, 'p_average_rating': 8.5},
         {'p_title': 'Genshin Impact',
          'p_description': 'Genshin Impact — приключенческая ролевая игра в открытом мире. Игроки исследуют фэнтезийный мир Тейвата, выполняя квесты, решая головоломки и сражаясь с врагами. Игра предлагает богатый выбор персонажей с уникальными способностями, глубокую систему прокачки и динамичные бои.',
          'p_release_date': '2020-09-28', 'p_developer_id': 3, 'p_genre_id': 4, 'p_average_rating': 9.5},
         {'p_title': 'Resident Evil 4',
          'p_description': 'Resident Evil 4 — культовая игра в жанре survival horror и action. В центре сюжета — Леон С. Кеннеди, агент, отправленный в Европу для спасения дочери президента США из лап загадочного культа. Игроков ждут напряженные сражения с мутантами, элементы выживания и исследование атмосферных локаций.',
          'p_release_date': '2023-03-24', 'p_developer_id': 4, 'p_genre_id': 5, 'p_average_rating': 9.3}]

game_platforms = [{'p_game_id': 1, 'p_platform_id': 1}, {'p_game_id': 1, 'p_platform_id': 3},
                  {'p_game_id': 1, 'p_platform_id': 5}, {'p_game_id': 2, 'p_platform_id': 1},
                  {'p_game_id': 2, 'p_platform_id': 6}, {'p_game_id': 2, 'p_platform_id': 7},
                  {'p_game_id': 3, 'p_platform_id': 1}, {'p_game_id': 3, 'p_platform_id': 7},
                  {'p_game_id': 4, 'p_platform_id': 1}, {'p_game_id': 4, 'p_platform_id': 3},
                  {'p_game_id': 4, 'p_platform_id': 4}, {'p_game_id': 4, 'p_platform_id': 5},
                  {'p_game_id': 5, 'p_platform_id': 1}, {'p_game_id': 5, 'p_platform_id': 3},
                  {'p_game_id': 5, 'p_platform_id': 5}, {'p_game_id': 5, 'p_platform_id': 6}]


# Функции для заполнения таблиц
def add_platforms():
    for platform in platforms:
        call_procedure("games.add_platform", platform)
    print("Platforms added successfully!")


def add_developers():
    for developer in developers:
        call_procedure("games.add_developer", developer)
    print("Developers added successfully!")


def add_genres():
    for genre in genres:
        call_procedure("games.add_genre", genre)
    print("Genres added successfully!")


def add_games():
    for game in games:
        call_procedure("games.add_game", game)
    print("Games added successfully!")


def add_game_platforms():
    for gp in game_platforms:
        call_procedure("games.add_game_platform", gp)
    print("Game-Platform relationships added successfully!")


def add_reviews():
    """Добавление записей в таблицу Reviews"""
    reviews = [
        {"p_game_id": 1, "p_user_id": 1, "p_rating": 9, "p_comment": "Great gameplay and graphics!"},
        {"p_game_id": 2, "p_user_id": 2, "p_rating": 8, "p_comment": "Interesting mechanics but repetitive."},
        {"p_game_id": 3, "p_user_id": 1, "p_rating": 10, "p_comment": "Masterpiece! Absolutely loved it."},
        {"p_game_id": 4, "p_user_id": 2, "p_rating": 7, "p_comment": "Fun but lacks depth in story."},
    ]
    for review in reviews:
        try:
            call_procedure("users.add_review", review)
            print(f"Review for GameID {review['p_game_id']} by UserID {review['p_user_id']} added successfully!")
        except Exception as e:
            print(f"Error adding review for GameID {review['p_game_id']} by UserID {review['p_user_id']}: {e}")


# Заполнение всех таблиц
def populate_database():
    add_users()
    add_platforms()
    add_developers()
    add_genres()
    add_games()
    add_game_platforms()
    add_reviews()
    print("Database populated successfully!")


# Выполнение заполнения
if __name__ == "__main__":
    populate_database()
