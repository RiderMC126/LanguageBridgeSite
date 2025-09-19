import asyncpg
import hashlib
from config import *

# =========================
# Инициализация базы данных
# =========================
async def init_db():
    """Инициализация базы данных и создание таблиц users и messages"""
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        # Таблица users
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Таблица messages
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender_id INT REFERENCES users(id) ON DELETE CASCADE,
                receiver_id INT REFERENCES users(id) ON DELETE CASCADE,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        print("База данных и таблицы успешно инициализированы.")
        await conn.close()

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")


# =========================
# Хэширование пароля
# =========================
async def hash_password(password: str) -> str:
    """
    Хэширование пароля с использованием SHA256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# =========================
# Регистрация пользователя
# =========================
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


# =========================
# Аутентификация пользователя
# =========================
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


# =========================
# Получить пользователей по поиску
# =========================
async def search_users(query: str, current_user: str):
    """
    Поиск пользователей по логину, кроме текущего пользователя.
    """
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        rows = await conn.fetch("""
            SELECT username FROM users
            WHERE username ILIKE $1 AND username != $2
            ORDER BY username ASC
            LIMIT 10
        """, f"%{query}%", current_user)

        await conn.close()
        return [r["username"] for r in rows]

    except Exception as e:
        print(f"Ошибка при поиске пользователей: {e}")
        return []


# =========================
# Получить пользователей с историей сообщений
# =========================
async def users_with_history(current_user: str):
    """
    Возвращает список пользователей, с которыми есть история переписки
    """
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        rows = await conn.fetch("""
            SELECT DISTINCT u.username
            FROM users u
            JOIN messages m ON u.id = m.sender_id OR u.id = m.receiver_id
            WHERE u.username != $1
              AND (m.sender_id = (SELECT id FROM users WHERE username=$1)
                   OR m.receiver_id = (SELECT id FROM users WHERE username=$1))
        """, current_user)

        await conn.close()
        return [r["username"] for r in rows]

    except Exception as e:
        print(f"Ошибка при получении пользователей с историей: {e}")
        return []


# =========================
# Сохранение сообщения
# =========================
async def save_message(sender: str, receiver: str, content: str):
    """
    Сохраняет сообщение в базе
    """
    try:
        conn = await asyncpg.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        sender_id = await conn.fetchval("SELECT id FROM users WHERE username=$1", sender)
        receiver_id = await conn.fetchval("SELECT id FROM users WHERE username=$1", receiver)

        if sender_id is None or receiver_id is None:
            await conn.close()
            return False

        await conn.execute(
            "INSERT INTO messages(sender_id, receiver_id, content) VALUES($1, $2, $3)",
            sender_id, receiver_id, content
        )
        await conn.close()
        return True

    except Exception as e:
        print(f"Ошибка при сохранении сообщения: {e}")
        return False

