from html import escape


def render_name_input_page() -> str:
    return """
    <html>
        <head>
            <meta charset=\"UTF-8\">
            <title>Game Start</title>
            <link rel=\"stylesheet\" href=\"/static/style.css\">
        </head>
        <body>
            <main class=\"container\">
                <h1>あなたの名前</h1>
                <form action=\"/setname\" method=\"post\" class=\"name-form\">
                    <input type=\"text\" name=\"player_name\" required>
                    <button type=\"submit\">Start Game</button>
                </form>
            </main>
        </body>
    </html>
    """


def render_game_page(player_name: str) -> str:
    safe_name = escape(player_name)
    return f"""
    <html>
        <head>
            <meta charset=\"UTF-8\">
            <title>Game Screen</title>
            <link rel=\"stylesheet\" href=\"/static/style.css\">
        </head>
        <body>
            <main class=\"container\">
                <h1>名前:{safe_name}</h1>
                <p>Click inside the canvas to increase your score.</p>
                <canvas id=\"gameCanvas\" width=\"800\" height=\"600\"></canvas>
                <p id=\"apiStatus\">API status: waiting...</p>
                <a href=\"/\" class=\"link\">Change name</a>
            </main>
            <script src=\"/static/game.js\"></script>
        </body>
    </html>
    """