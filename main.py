from sqlalchemy import create_engine, text
from config import dbname, user, password, host, port

if __name__ == '__main__':
    DATABASE_URL = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(DATABASE_URL)

    # Работет ли эта хуйня
    with engine.connect() as conn:
        result = conn.execute(text('SELECT version();'))
        for row in result:
            print(f'PostgreSQL Version: {row[0]}')
