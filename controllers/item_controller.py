from database.db import get_db_connection
from models.item_model import ItemCreate, ItemResponse
from models.response_model import ResponseModel
from exceptions.custom_exception import CustomException
import logging
import aiomysql

# Inisialisasi logger
logger = logging.getLogger(__name__)


async def get_all_items():
    try:
        async with get_db_connection() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT id, name, description, price FROM items")
                result = await cursor.fetchall()
                items = [ItemResponse(id=row['id'], name=row['name'],
                                      description=row['description'], price=row['price']) for row in result]
                return ResponseModel(
                    error="false",
                    code="200",
                    message="get data success",
                    data=items
                )
    except Exception as e:
        logger.error(f"Error fetching all items: {e}")
        raise CustomException(
            status_code=500,
            detail="Error while fetching items"
        )


async def create_item(item: ItemCreate):
    try:
        async with get_db_connection() as conn:
            async with conn.cursor() as cursor:
                sql = "INSERT INTO items (name, description, price) VALUES (%s, %s, %s)"
                await cursor.execute(sql, (item.name, item.description, item.price))
                await conn.commit()
                item_id = cursor.lastrowid
                created_item = ItemResponse(
                    id=item_id, name=item.name, description=item.description, price=item.price)
                return ResponseModel(
                    error="false",
                    code="201",
                    message="Item created successfully",
                    data=[created_item]
                )
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise CustomException(
            status_code=500,
            detail="Error while creating item"
        )


async def get_item_by_id(item_id: int):
    try:
        async with get_db_connection() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                sql = "SELECT id, name, description, price FROM items WHERE id = %s"
                await cursor.execute(sql, (item_id,))
                row = await cursor.fetchone()
                if not row:
                    raise CustomException(
                        status_code=404,
                        detail="Item not found"
                    )
                item = ItemResponse(
                    id=row['id'], name=row['name'], description=row['description'], price=row['price'])
                return ResponseModel(
                    error="false",
                    code="200",
                    message="get data success",
                    data=item
                )
    except CustomException as ce:
        logger.error(f"CustomException: {ce.detail}")
        raise ce
    except Exception as e:
        logger.error(f"Error fetching item by ID: {e}")
        raise CustomException(
            status_code=500,
            detail="Error while fetching item"
        )


async def delete_item(item_id: int):
    try:
        async with get_db_connection() as conn:
            async with conn.cursor() as cursor:
                sql = "DELETE FROM items WHERE id = %s"
                await cursor.execute(sql, (item_id,))
                if cursor.rowcount == 0:
                    raise CustomException(
                        status_code=404,
                        detail="Item not found"
                    )
                await conn.commit()
                return ResponseModel(
                    error="false",
                    code="200",
                    message="Item deleted successfully",
                    data=[]
                )
    except CustomException as ce:
        logger.error(f"CustomException: {ce.detail}")
        raise ce
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        raise CustomException(
            status_code=500,
            detail="Error while deleting item"
        )
