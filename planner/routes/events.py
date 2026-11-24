from typing import List

from fastapi import APIRouter, Body, HTTPException, status

from models.events import Event

event_router = APIRouter(tags=["Events"])

# Временное хранилище событий (в памяти процесса)
events: List[Event] = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    """Получение списка всех событий."""
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    """Получение события по идентификатору."""
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Событие с указанным идентификатором не существует",
    )


@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event = Body(...)) -> dict:
    """Создание нового события."""
    events.append(body)
    return {"message": "Событие успешно создано"}


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    """Удаление события по идентификатору."""
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Событие успешно удалено"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Событие с указанным идентификатором не существует",
    )


@event_router.delete("/")
async def delete_all_events() -> dict:
    """Удаление всех событий."""
    events.clear()
    return {"message": "Все события успешно удалены"}
