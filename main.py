from fastapi import FastAPI
from data.database import init_database
from routers.movies import movies_router
from routers.users import users_router

init_database()

app = FastAPI()

app.include_router(movies_router)
app.include_router(users_router)