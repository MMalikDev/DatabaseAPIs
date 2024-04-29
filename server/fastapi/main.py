import uvicorn
from configs.core import settings
from database import lifespan
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from router import Login, UsersController, router

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.host(settings.STATIC_URL, StaticFiles(), name="static")


def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, name="index.html")


# Root
app.add_api_route("/", index, response_class=HTMLResponse)
app.include_router(Login.router, tags=["login"])
app.include_router(router, tags=["api"], prefix="/api")
app.include_router(UsersController.router, tags=["users"], prefix="/users")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.WEB_HOST, port=settings.WEB_PORT)
