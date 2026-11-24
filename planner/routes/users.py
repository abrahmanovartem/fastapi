from fastapi import APIRouter, HTTPException, status

from models.users import NewUser, UserSignIn

user_router = APIRouter(
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

# Временное хранилище пользователей (в памяти процесса)
users: dict[str, NewUser] = {}


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_new_user(data: NewUser) -> dict:
    """Регистрация нового пользователя."""
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким адресом электронной почты уже существует",
        )
    users[data.email] = data
    return {"message": "Пользователь успешно зарегистрирован"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    """Вход пользователя по email и паролю."""
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не существует",
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Передан неверный пароль",
        )
    return {"message": "Вход выполнен успешно"}


@user_router.post("/signout")
async def sign_user_out(user: UserSignIn) -> dict:
    """Выход пользователя.

    Приложение не поддерживает сессии на текущем этапе, поэтому маршрут
    лишь подтверждает операцию выхода.
    """
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не существует",
        )
    return {"message": "Выход выполнен успешно"}
