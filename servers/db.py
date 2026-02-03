import aiosqlite
import os

DB_PATH = os.getenv("DB_PATH", "app.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица продуктов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                in_stock BOOLEAN DEFAULT 1
            )
        """)
        # Таблица заказов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT DEFAULT 'created',
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """)
        await db.commit()


def get_db_path():
    return DB_PATH
