from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItems

todo_router = APIRouter()

todo_list = []

# Инициализация шаблонов Jinja из папки templates/
templates = Jinja2Templates(directory="templates/")


@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"request": request, "todos": todo_list}
    )


@todo_router.get("/todo")
async def retrieve_todos(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"request": request, "todos": todo_list}
    )


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    request: Request,
    todo_id: int =Path(..., title="Todo ID", gt=0)
):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={"request": request, "todo": todo}
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} not found."
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: Todo, todo_id: int = Path(..., gt=0)) -> dict:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list[index] = todo_data
            return {
                "message": f"Todo with ID {todo_id} updated successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} does not exist."
    )


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int = Path(..., gt=0)) -> dict:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": f"Todo with ID {todo_id} deleted successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} not found."
    )