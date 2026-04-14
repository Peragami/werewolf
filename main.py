# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>FastAPIブラウザ表示test</title>
        </head>
        <body>
            <h1>FastAPIでブラウザに表示しています</h1>
            <p>このページはFastAPIから返されたHTMLです。</p>
        </body>
    </html>
    """