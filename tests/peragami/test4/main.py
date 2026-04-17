from pathlib import Path
import time
import urllib.parse
import uuid
from collections.abc import Mapping

from fastapi import FastAPI, Form, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from .frontend import render_game_page, render_name_input_page
except ImportError:
    from frontend import render_game_page, render_name_input_page


class ScoreRequest(BaseModel):
    score: int


app = FastAPI(title="Werewolf App", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

SESSION_COOKIE_KEY = "session_id"
ACTIVE_WINDOW_SECONDS = 300
connected_players: dict[str, dict[str, str | float | int]] = {}
player_score_history: dict[str, int] = {}
player_stream_connections: set[WebSocket] = set()


def cleanup_inactive_players(now: float) -> None:
    inactive_sessions = [
        session_id
        for session_id, player_data in connected_players.items()
        if now - float(player_data["last_seen"]) > ACTIVE_WINDOW_SECONDS
    ]
    for session_id in inactive_sessions:
        del connected_players[session_id]


def touch_player_session_by_cookies(
    cookies: Mapping[str, str], score: int | None = None
) -> None:
    session_id = cookies.get(SESSION_COOKIE_KEY)
    if not session_id:
        return

    existing_data = connected_players.get(session_id, {})
    encoded_name = cookies.get("player_name")
    player_name = (
        urllib.parse.unquote(encoded_name)
        if encoded_name
        else str(existing_data.get("name", "Guest"))
    )
    if score is None:
        current_score = int(
            existing_data.get("score", player_score_history.get(player_name, 0))
        )
    else:
        current_score = score

    connected_players[session_id] = {
        "name": player_name,
        "score": current_score,
        "last_seen": time.time(),
    }
    player_score_history[player_name] = current_score


def touch_player_session(request: Request, score: int | None = None) -> None:
    touch_player_session_by_cookies(request.cookies, score=score)


def get_connected_players(now: float) -> list[dict[str, str | int]]:
    cleanup_inactive_players(now)
    return [
        {
            "name": str(player_data["name"]),
            "score": int(player_data.get("score", 0)),
        }
        for player_data in connected_players.values()
    ]


async def broadcast_connected_players() -> None:
    payload = {"type": "players", "players": get_connected_players(time.time())}
    dead_connections: list[WebSocket] = []

    for websocket in list(player_stream_connections):
        try:
            await websocket.send_json(payload)
        except Exception:
            dead_connections.append(websocket)

    for websocket in dead_connections:
        player_stream_connections.discard(websocket)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    encoded_name = request.cookies.get("player_name")
    player_name = urllib.parse.unquote(encoded_name) if encoded_name else ""
    return render_name_input_page(player_name)


@app.post("/setname")
async def set_player_name(request: Request, player_name: str = Form(...)):
    encoded_name = urllib.parse.quote(player_name)
    response = RedirectResponse(url="/game", status_code=303)
    response.set_cookie(key="player_name", value=encoded_name, max_age=86400)

    session_id = request.cookies.get(SESSION_COOKIE_KEY) or uuid.uuid4().hex
    response.set_cookie(key=SESSION_COOKIE_KEY, value=session_id, max_age=86400)

    now = time.time()
    cleanup_inactive_players(now)
    existing_score = int(connected_players.get(session_id, {}).get("score", 0))
    restored_score = int(player_score_history.get(player_name, existing_score))
    connected_players[session_id] = {
        "name": player_name,
        "score": restored_score,
        "last_seen": now,
    }
    player_score_history[player_name] = restored_score
    await broadcast_connected_players()
    return response


@app.get("/game", response_class=HTMLResponse)
def game_page(request: Request):
    encoded_name = request.cookies.get("player_name")
    player_name = urllib.parse.unquote(encoded_name) if encoded_name else "Guest"

    now = time.time()
    touch_player_session(request)
    players = get_connected_players(now)
    return render_game_page(player_name, players)


@app.post("/api/score")
async def update_score(request: Request, score_data: ScoreRequest):
    touch_player_session(request, score=score_data.score)
    await broadcast_connected_players()
    print(f"Received score: {score_data.score}")
    return {"message": "Score updated", "score": score_data.score}


@app.get("/api/connected-users")
def connected_users(request: Request):
    touch_player_session(request)
    now = time.time()
    return {"players": get_connected_players(now)}


@app.get("/api/me")
def current_player(request: Request):
    touch_player_session(request)
    session_id = request.cookies.get(SESSION_COOKIE_KEY)
    if not session_id:
        return {"name": "Guest", "score": 0}

    player_data = connected_players.get(session_id)
    if not player_data:
        return {"name": "Guest", "score": 0}

    return {
        "name": str(player_data.get("name", "Guest")),
        "score": int(player_data.get("score", 0)),
    }


@app.post("/api/disconnect")
async def disconnect(request: Request):
    session_id = request.cookies.get(SESSION_COOKIE_KEY)
    if session_id and session_id in connected_players:
        del connected_players[session_id]
        await broadcast_connected_players()
    return {"ok": True}


@app.websocket("/ws/players")
async def players_websocket(websocket: WebSocket):
    await websocket.accept()
    player_stream_connections.add(websocket)

    # Push current snapshot immediately after connect.
    await websocket.send_json(
        {"type": "players", "players": get_connected_players(time.time())}
    )

    try:
        while True:
            message = await websocket.receive_text()
            if message == "ping":
                touch_player_session_by_cookies(websocket.cookies)
    except WebSocketDisconnect:
        pass
    finally:
        player_stream_connections.discard(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
