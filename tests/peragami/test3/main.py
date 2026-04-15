from pathlib import Path
import urllib.parse

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from .frontend import render_game_page, render_name_input_page
except ImportError:
    from frontend import render_game_page, render_name_input_page


class ScoreRequest(BaseModel):
    score: int


app = FastAPI(title="Werewolf Mixed App", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


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


@app.post("/api/score")
async def update_score(score_data: ScoreRequest):
    print(f"Received score: {score_data.score}")
    return {"message": "Score updated", "score": score_data.score}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)