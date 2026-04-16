# 2D3D人狼プロジェクト

役職を活用して戦うソーシャル推理ゲーム（人狼）を開発するプロジェクトです。  
本 README は、`2D3D人狼作成指示書.md` と旧 `README.md` の内容を統合したものです。

## 1. プロジェクト概要

- タイトル: 役職もりもり人狼（仮）
- ジャンル: Social Deduction Game
- 目的: プレイヤーは村人側または人狼側に分かれ、役職の能力を活用して勝利を目指す
- プラットフォーム: PC
- ターゲット: 15歳以上の推理ゲーム愛好者

## 2. ゲーム基本ルール

- プレイ人数: 6〜12人
- 進行: 昼（議論・投票）→ 夜（役職アクション）を繰り返す
- 勝利条件:
  - 白陣営: 人狼の全滅
  - 黒陣営: 村人の人数が人狼以下になる
  - 特殊陣営: 各役職固有の条件に従う

## 3. ゲームフロー

- 開始: 役職割り当て、役職カード表示
- 昼: 3分議論し、投票で追放
- 夜: 役職アクションを選択
- 終了: 結果発表

## 4. 実装機能（現在）

- スキップ機能
  - プレイヤーがその日の役職行動を終えたらスキップできる
- Bot追加機能
  - テストプレイ時に人数不足を補うため、人数指定でBotを追加できる
  - Bot名はランダムに割り当てる
  - 基本役職の行動終了後にスキップへ移行できる

## 5. 技術要件

- 言語: Python
- フレームワーク: FastAPI
- Pythonバージョン: 3.12.10（推奨）

### 主なパッケージ

- fastapi
- uvicorn
- pydantic
- python-multipart

## 6. 開発環境構築

### 6.1 Python仮想環境（Windows / PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 6.2 アプリ起動（ローカル）

`src/main.py` を利用して起動します。

```powershell
uvicorn src.main:app --reload
```

または:

```powershell
python src/main.py
```

## 7. Dockerでの起動

```powershell
docker compose up --build
```

## 8. ディレクトリ構成（抜粋）

```text
werewolf/
├─ src/
│  ├─ main.py
│  ├─ frontend.py
│  └─ static/
├─ tests/
├─ requirements.txt
├─ Dockerfile
└─ docker-compose.yml
```

## 9. 今後の実装候補

- LLMモデルを使った対話可能なBotの実装
- UI/UX改善（2D/3D演出の強化）
- 役職・陣営バランスの調整機能

