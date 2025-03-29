from fastapi import FastAPI, APIRouter
from app.api.routers.auth import auth_route
from app.db import create_tables

router = APIRouter()

app = FastAPI()
app.include_router(auth_route)


app.add_event_handler("startup", create_tables)


@router.get('/')
def main():
    return 'Тестовое API'
