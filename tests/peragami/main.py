from pathlib import Path
import urllib.parse

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

try:
    from .frontend import render_game_page, render_name_input_page
except ImportError:
    from tests.peragami.frontend import render_game_page, render_name_input_page

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root():
    return render_name_input_page()


@app.post("/setname")
def set_player_name(player_name: str = Form(...)):
    encoded_name = urllib.parse.quote(player_name)
    response = RedirectResponse(url="/game", status_code=303)
    response.set_cookie(key="player_name", value=encoded_name, max_age=86400)
    return response


@app.get("/game", response_class=HTMLResponse)
def game_page(request: Request):
    encoded_name = request.cookies.get("player_name")
    player_name = urllib.parse.unquote(encoded_name) if encoded_name else "Guest"
    return render_game_page(player_name)