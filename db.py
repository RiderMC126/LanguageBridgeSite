import asyncpg
import asyncio
import hashlib
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

async def hash_password(password: str) -> str:
    """
    Хэширование пароля с использованием SHA256.
    """
    return hashlib.sha256(password.encode()).hexdigest()

async def register_user(username: str, email: str, password: str):
    """
    Добавление нового пользователя в базу.
    Возвращает tuple (success: bool, message: str)
    """
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        hashed = await hash_password(password)
        await conn.execute("""
            INSERT INTO users(username, email, password)
            VALUES($1, $2, $3)
        """, username, email, hashed)
        await conn.close()
        return True, "User registered successfully"
    except asyncpg.exceptions.UniqueViolationError:
        return False, "Username or email already exists"
    except Exception as e:
        return False, f"Database error: {e}"


async def authenticate_user(login_or_email: str, password: str):
    """
    Проверка логина/почты и пароля.
    Возвращает tuple (success: bool, message: str)
    """
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        hashed = await hash_password(password)
        if "@" in login_or_email:
            user = await conn.fetchrow("""
                SELECT * FROM users WHERE email=$1 AND password=$2
            """, login_or_email, hashed)
        else:
            user = await conn.fetchrow("""
                SELECT * FROM users WHERE username=$1 AND password=$2
            """, login_or_email, hashed)
        await conn.close()
        if user:
            return True, "Login successful"
        return False, "Invalid login/email or password"
    except Exception as e:
        return False, f"Database error: {e}"

