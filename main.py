# main.py
from fastapi import FastAPI
from controllers import category_controller, product_controller, order_controller, auth_controller, user_controller
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="FastAPI Store")

app.include_router(category_controller.router)
app.include_router(product_controller.router)
app.include_router(order_controller.router)
app.include_router(auth_controller.router)
app.include_router(user_controller.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    infor = {
        "name": "Hoang Hai",
        "age": 28,
        "skills": ["Python","FastAPI","Database"]
    }

