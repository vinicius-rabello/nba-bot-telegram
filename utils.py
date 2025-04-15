from datetime import datetime

def format_games_message(games_data):
    if not games_data:
        return "Não há jogos marcados para essa data."
    
    # Extract date from first game (assuming all same date)
    game_date = games_data[0][1].strftime('%B %d, %Y')
    
    message = [f"🗓 *Jogos em {game_date}* 🗓\n"]
    
    for game in games_data:
        (_, _, game_time, broadcaster, home_team, away_team, 
         home_team_score, away_team_score, venue, city, state) = game
        
        # Format game time
        if "FINAL" not in game_time:
            game_time = datetime.strptime(game_time, '%H:%M').strftime('%I:%M %p ET')

        gamecard = f"\n🏀 *{home_team} vs {away_team}*"
        if home_team_score and away_team_score:
            gamecard = f"\n🏀 *{home_team} {home_team_score} vs {away_team_score} {away_team}*"
        
        game_info = [
            gamecard,
            f"⏰ {game_time}",
            f"📍 {venue}, {city}, {state}",
            f"📺 {broadcaster}" if broadcaster else "📺 Unknown"
        ]
        
        message.append("\n".join(game_info))
    
    return "\n".join(message)