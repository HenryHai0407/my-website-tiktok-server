# main.py
from fastapi import FastAPI
from routers.router import routes
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="FastAPI Store")

app.include_router(routes)

@app.get("/")
async def index(request: Request):
    return {
        "name": "Hoang Hai",
        "age": 28,
        "skills": ["Python","FastAPI","Database","Docker"]
    }
    

