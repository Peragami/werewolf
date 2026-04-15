# main.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI(title="ブラウザゲームAPI", version="1.0.0")

# スコアを受け取るためのリクエストモデル
class ScoreRequest(BaseModel):
    score: int

# 静的ファイル（HTML, JS, CSSなど）を配信
# プロジェクト構成例:
# project/
# ├── main.py
# └── static/
#     ├── index.html
#     └── game.js
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ルートパスで index.html を返す
@app.get("/")
async def read_index():
    return FileResponse(STATIC_DIR / "index.html")

# スコアを受け取るAPIエンドポイント
@app.post("/api/score")
async def update_score(score_data: ScoreRequest):
    # ここでスコアをデータベースに保存したり、処理したりします
    print(f"受信したスコア: {score_data.score}")
    return {"message": "スコアを受信しました", "score": score_data.score}

# 開発用にサーバーを起動する場合のエントリーポイント
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
