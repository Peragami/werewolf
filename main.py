from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import urllib.parse

app = FastAPI()

# プレイヤー名を入力するフォームを表示
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head><title>ゲーム登録</title></head>
        <body>
            <h1>プレイヤー名を入力してください</h1>
            <form action="/setname" method="post">
                <input type="text" name="player_name" required>
                <button type="submit">保存してゲーム開始</button>
            </form>
        </body>
    </html>
    """

# フォーム送信を受け取り、Cookieに保存 → ゲーム画面へ
@app.post("/setname")
def set_player_name(player_name: str = Form(...)):
    encoded_name = urllib.parse.quote(player_name)

    response = RedirectResponse(url="/game", status_code=303)
    response.set_cookie(
        key="player_name",
        value=encoded_name,
        max_age=86400
    )
    return response

# ゲーム画面
@app.get("/game", response_class=HTMLResponse)
def game_page(request: Request):
    encoded_name = request.cookies.get("player_name")

    if encoded_name:
        player_name = urllib.parse.unquote(encoded_name)
    else:
        player_name = "ゲスト"

    return f"""
    <html>
        <head><title>ゲーム画面</title></head>
        <body>
            <h1>ようこそ、{player_name} さん！</h1>
            <p>名前変更実装完了</p>
            <a href="/">名前をやり直す</a>
        </body>
    </html>
    """