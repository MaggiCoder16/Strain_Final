def extract_valid_games(games_ndjson):
    valid_pgns = []
    for line in games_ndjson:
        try:
            game = json.loads(line)
        except json.JSONDecodeError:
            continue

        if game.get("variant") != "chess960":
            continue

        players = game.get("players", {})
        white = players.get("white", {})
        black = players.get("black", {})
        white_user = white.get("user", {})
        black_user = black.get("user", {})

        if not (white_user.get("bot") and black_user.get("bot")):
            continue

        white_rating, white_prov = parse_rating(white)
        black_rating, black_prov = parse_rating(black)

        # Allow provisional games and games with rating >= 2400
        white_ok = white_prov or white_rating >= 2400
        black_ok = black_prov or black_rating >= 2400

        if white_ok and black_ok and "pgn" in game:
            valid_pgns.append(game["pgn"].strip())

    return valid_pgns
