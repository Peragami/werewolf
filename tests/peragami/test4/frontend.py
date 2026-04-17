from html import escape


def render_name_input_page(default_player_name: str = "") -> str:
    safe_default_name = escape(default_player_name)
    return f"""
    <html>
        <head>
            <meta charset=\"UTF-8\">
            <title>Game Start</title>
            <link rel=\"stylesheet\" href=\"/static/style.css\">
        </head>
        <body>
            <main class=\"container\">
                <h1>Player Name</h1>
                <form action=\"/setname\" method=\"post\" class=\"name-form\">
                    <input type=\"text\" name=\"player_name\" value=\"{safe_default_name}\" required>
                    <button type=\"submit\">Next</button>
                </form>
            </main>
        </body>
    </html>
    """


def render_game_page(player_name: str, connected_players: list[dict[str, str | int]]) -> str:
    safe_name = escape(player_name)
    connected_name_items = "".join(
        f"<li>{escape(str(player.get('name', 'Guest')))} : {int(player.get('score', 0))}</li>"
        for player in connected_players
    ) or "<li>No players</li>"

    return f"""
    <html>
        <head>
            <meta charset=\"UTF-8\">
            <title>Game Screen</title>
            <link rel=\"stylesheet\" href=\"/static/style.css\">
        </head>
        <body>
            <main class=\"container\">
                <h1>Player: {safe_name}</h1>
                <section class=\"connected-section\">
                    <h2>Currently Connected Players</h2>
                    <ul id=\"connectedUsers\" class=\"connected-users\">
                        {connected_name_items}
                    </ul>
                </section>
                <p>Click inside the canvas to increase score.</p>
                <canvas id=\"gameCanvas\" width=\"800\" height=\"600\"></canvas>
                <p id=\"apiStatus\">API status: waiting...</p>
                <a href=\"/\" class=\"link\">Back</a>
            </main>
            <script src=\"/static/game.js\"></script>
        </body>
    </html>
    """
