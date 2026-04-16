# ベースイメージ（例: Python 3.11）。必要に応じて変更。
FROM python:3.11-slim

# 作業ディレクトリをコンテナ内に作成
WORKDIR /app

# リポジトリの内容をコンテナの /app にコピー
COPY . .

# Python パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# コンテナ起動時に実行するコマンド（main.py を起動）
CMD ["python", "src/main.py"]
