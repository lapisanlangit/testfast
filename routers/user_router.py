from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.user_controller import get_user, get_all_users, create_user
from schemas.user_schema import UserCreate
from database import get_db
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await get_user(db, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        data = {
            "error": "false",
            "code": "200",
            "message": "get data success sekali",
            "data": user
        }
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        # Tangani HTTPException (misalnya, 404 Not Found)
        data = {
            "error": "true",
            "code": str(e.status_code),
            "message": e.detail,
            "data": None
        }
        return JSONResponse(content=data, status_code=e.status_code)
    except Exception as e:
        # Tangani exception lainnya (misalnya, 500 Internal Server Error)
        data = {
            "error": "true",
            "code": "500",
            "message": "Internal server error",
            # Hati-hati, jangan expose detail error ke client di production
            "data": str(e)
        }
        return JSONResponse(content=data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     try:
#         user = await get_user(db, user_id)
#         data = {
#             "error": "false",
#             "code": "200",
#             "message": "get data success",
#             "data": user
#         }
#         return JSONResponse(content=data, status_code=status.HTTP_200_OK)
#     except Exception as e:
#         data = {
#             "error": "true",
#             "code": "500",
#             "message": "error data",
#             "data": e
#         }
#     return data
#


@router.get("/users/")
async def read_all_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db, skip=skip, limit=limit)
    return users


@router.post("/users/")
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)
