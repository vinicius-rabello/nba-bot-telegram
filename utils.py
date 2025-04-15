from datetime import datetime

# Dicionário de meses em português
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def format_games_message(games_data):
    if not games_data:
        return "Não há jogos marcados para essa data."

    # Extrair data do primeiro jogo
    game_date = games_data[0][1]
    formatted_date = f"{game_date.day} de {MESES_PT[game_date.month].capitalize()} de {game_date.year}"
    
    message = [f"🗓 *Jogos em {formatted_date}* 🗓\n"]
    
    for game in games_data:
        (_, _, game_time, broadcaster, home_team, away_team, 
         home_team_score, away_team_score, venue, city, state) = game
        
        # Format game time
        if "FINAL" not in game_time:
            game_time = datetime.strptime(game_time, '%H:%M')

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