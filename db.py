import asyncpg
import asyncio
from config import *


async def init_db():
    """Инициализация базы данных и создание таблицы users"""
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        # Проверяем существует ли таблица
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)

        if table_exists:
            print("Таблица 'users' уже существует.")
        else:
            await conn.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Таблица 'users' успешно создана.")

        await conn.close()
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")


# Для тестового запуска напрямую
if __name__ == "__main__":
    asyncio.run(init_db())
