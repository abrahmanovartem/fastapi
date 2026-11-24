from fastapi import FastAPI
from todo import todo_router

app = FastAPI(
    title="FastAPI Приложение",
    description="Практическое занятие"
)


@app.get("/")
async def welcome() -> dict:

    return {
        "message": "Добро пожаловать"
    }

app.include_router(todo_router)