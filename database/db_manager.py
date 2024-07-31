from sqlalchemy import String, BigInteger
from asyncpg_lite import DatabaseManager
from config_data.config import Config, load_config

config: Config = load_config()

db_manager = DatabaseManager(
    db_url=config.database.source,
    deletion_password=config.database.password,
)


async def create_table_users(table_name="tg_users"):
    """Создает таблицу для хранения пользователей."""
    async with db_manager as client:
        columns = [
            {
                "name": "user_id",
                "type": BigInteger,
                "options": {"primary_key": True, "autoincrement": False},
            },
            {"name": "full_name", "type": String},
            {"name": "user_login", "type": String},
            {"name": "city", "type": String},
        ]
        await client.create_table(table_name=table_name, columns=columns)


async def get_user_data(user_id: int, table_name="tg_users"):
    """Возвращает информацию о конкретном пользователе.\n
    На вход принимает айди пользователя
    """
    async with db_manager as client:
        user_data = await client.select_data(
            table_name=table_name, where_dict={"user_id": user_id}, one_dict=True
        )
    return user_data


async def insert_user(
    user_data: dict, table_name="tg_users", conflict_column="user_id"
):
    """Добавляет пользователя в базу данных.\n
    На вход принимает словарь с данными о пользователе:\n
    user_id: int\n
    full_name: str\n
    user_login: str\n
    city: str
    """
    async with db_manager as client:
        await client.insert_data_with_update(
            table_name=table_name,
            records_data=user_data,
            conflict_column=conflict_column,
            update_on_conflict=False,
        )


async def change_user_city(user_id: int, city: str, table_name="tg_users"):
    """Изменяет город пользователя в базе данных."""
    async with db_manager as client:
        await client.update_data(
            table_name=table_name,
            where_dict={"user_id": user_id},
            update_dict={"city": city},
        )
