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
            <h1>Please enter your player name</h1>
            <form action=\"/setname\" method=\"post\">
                <input type=\"text\" name=\"player_name\" required>
                <button type=\"submit\">Start Game</button>
            </form>
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
            <h1>Welcome, {safe_name}!</h1>
            <p>The game is preparing...</p>
            <a href=\"/\">Change name</a>
        </body>
    </html>
    """