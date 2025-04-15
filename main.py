from telegram.ext import Application, CommandHandler, MessageHandler, filters
from database.db import get_by_date
from utils import format_games_message
from datetime import datetime, timedelta
from config.settings import TELEGRAM_BOT_TOKEN
from pytz import timezone
from telegram import BotCommand
import dateparser

# This bot is a simple Telegram bot that provides information about NBA games.
async def set_commands(application):
    commands = [
        BotCommand('start', 'Instruções do bot'),
        BotCommand('jogos', 'Ver jogos de hoje ou outra data'),
    ]
    await application.bot.set_my_commands(commands)

# Helper to parse the date from arguments
def parse_date(args):
    brazil_tz = timezone('America/Sao_Paulo')
    today = datetime.now(brazil_tz).date()
    if not args:
        return today
    arg = args[0].lower()
    if arg == 'hoje':
        return today
    elif arg == 'ontem':
        return today - timedelta(days=1)
    elif arg == 'amanha' or arg == 'amanhã':
        return today + timedelta(days=1)
    else:
        try:
            return datetime.strptime(arg, '%Y-%m-%d').date()
        except ValueError:
            return None

async def start(update, context):
    message = (
        "🏀 Olá! Eu sou o *Bot da NBA* e estou aqui pra te mostrar os jogos da liga! 🇺🇸🔥\n\n"
        "Você pode usar os seguintes comandos:\n\n"
        "• `/jogos` — mostra os jogos de *hoje*\n"
        "• `/jogos hoje` — também mostra os jogos de *hoje*\n"
        "• `/jogos ontem` — jogos de *ontem*\n"
        "• `/jogos amanha` — jogos de *amanhã*\n"
        "• `/jogos YYYY-MM-DD` — jogos de uma *data específica* (ex: `/jogos 2025-04-15`)\n\n"
        "📌 *Importante:* o bot só mostra jogos até *amanhã*. Datas futuras ainda não estão disponíveis.\n\n"
        "Fique à vontade para explorar e acompanhar os confrontos da temporada! 🏆"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

async def jogos(update, context):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    date = parse_date(context.args)
    if date is None:
        await update.message.reply_text("❌ Formato de data inválido. Use `YYYY-MM-DD`, ou use palavras como `hoje`, `ontem`, `amanha`.", parse_mode='Markdown')
        return

    if date > tomorrow:
        await update.message.reply_text("🔒 Só tenho os jogos até amanhã. Tente uma data mais próxima!", parse_mode='Markdown')
        return

    games_data = get_by_date(date)
    message = format_games_message(games_data)
    await update.message.reply_text(message, parse_mode='Markdown')

async def jogos_texto(update, context):
    text = update.message.text.lower().strip()
    
    # Initialize date variable
    date = None
    brazil_tz = timezone('America/Sao_Paulo')
    today = datetime.now(brazil_tz).date()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    
    # Simple case: just "jogos" means today's games
    if text == "jogos":
        date = today
    
    # Check for keywords (hoje, ontem, amanhã) anywhere in the text
    elif "hoje" in text:
        date = today
    elif "ontem" in text:
        date = yesterday
    elif "amanha" in text or "amanhã" in text:
        date = tomorrow
    
    # If no keywords found, try to extract date using regex patterns
    else:
        # Try to match various date formats using regex
        import re
        
        # Format: YYYY-MM-DD (ISO format)
        iso_match = re.search(r'\b(\d{4}-\d{1,2}-\d{1,2})\b', text)
        if iso_match:
            try:
                date = datetime.strptime(iso_match.group(1), '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Format: DD/MM/YYYY or DD-MM-YYYY
        if not date:
            dmy_match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', text)
            if dmy_match:
                try:
                    day, month, year = int(dmy_match.group(1)), int(dmy_match.group(2)), int(dmy_match.group(3))
                    date = datetime(year, month, day).date()
                except ValueError:
                    pass
        
        # Format: DD/MM or DD-MM (assume current year or previous year if date would be in the future)
        if not date:
            dm_match = re.search(r'\b(\d{1,2})[/-](\d{1,2})\b', text)
            if dm_match:
                try:
                    day, month = int(dm_match.group(1)), int(dm_match.group(2))
                    # First try with current year
                    candidate_date = datetime(today.year, month, day).date()
                    # If the date would be in the future (beyond tomorrow), use previous year
                    if candidate_date > tomorrow:
                        candidate_date = datetime(today.year - 1, month, day).date()
                    date = candidate_date
                except ValueError:
                    pass
        
        # Format: "dia DD de mês" (e.g., "dia 15 de abril")
        if not date:
            months = {
                'janeiro': 1, 'fevereiro': 2, 'março': 3, 'marco': 3, 'abril': 4,
                'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9,
                'outubro': 10, 'novembro': 11, 'dezembro': 12
            }
            
            # Pattern for "DD de mês" or "dia DD de mês"
            day_month_match = re.search(r'\b(?:dia\s+)?(\d{1,2})\s+(?:de\s+)?(\w+)(?:\s+(?:de\s+)?(\d{4}))?\b', text)
            if day_month_match:
                day = int(day_month_match.group(1))
                month_name = day_month_match.group(2).lower()
                year_str = day_month_match.group(3)
                
                if month_name in months:
                    month = months[month_name]
                    
                    # If year was explicitly specified, use it
                    if year_str:
                        year = int(year_str)
                    else:
                        # If no year specified, use current year
                        year = today.year
                        
                        # Check if the date would be in the future (beyond tomorrow)
                        try:
                            candidate_date = datetime(year, month, day).date()
                            if candidate_date > tomorrow:
                                # If it's for a future date beyond tomorrow, assume previous year
                                year = today.year - 1
                        except ValueError:
                            # If date is invalid (e.g., Feb 30), just continue with default year
                            pass
                    
                    try:
                        date = datetime(year, month, day).date()
                    except ValueError:
                        # Invalid date, like February 30
                        pass
    
    # If all parsing attempts fail, try dateparser as a fallback
    if not date:
        parsed_date = dateparser.parse(
            text, 
            settings={
                'PREFER_DATES_FROM': 'past',
                'DATE_ORDER': 'DMY',
                'TIMEZONE': 'America/Sao_Paulo',
                'RELATIVE_BASE': datetime.now(brazil_tz),
            }
        )
        
        if parsed_date:
            date = parsed_date.date()
            # Double-check if dateparser returned a future date beyond tomorrow
            if date > tomorrow:
                # Try to adjust the year to make it a past date
                try:
                    date = date.replace(year=date.year - 1)
                except ValueError:
                    # Handle edge cases like Feb 29 in leap years
                    pass
    
    # If we still don't have a date, tell the user we couldn't understand
    if not date:
        await update.message.reply_text(
            "🤔 Não entendi a data que você quer. Tente algo como:\n"
            "• *jogos hoje*\n"
            "• *jogos de ontem*\n"
            "• *jogos amanhã*\n"
            "• *jogos 15/04/2025*\n"
            "• *jogos do dia 15 de abril*",
            parse_mode='Markdown'
        )
        return
    
    # Check if date is in the allowed range
    if date > tomorrow:
        await update.message.reply_text(
            "🔒 Só tenho os jogos até amanhã. Tente uma data mais próxima!",
            parse_mode='Markdown'
        )
        return
    
    # Get and format game data
    games_data = get_by_date(date)
    message = format_games_message(games_data)
    await update.message.reply_text(message, parse_mode='Markdown')

def main():
    print("Starting bot...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('jogos', jogos))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, jogos_texto))


    # Set autocomplete commands
    application.post_init = set_commands  # This will run the set_commands function when the app initializes

    print("Bot initialized, starting polling...")
    application.run_polling()
    print("Polling started")

if __name__ == '__main__':
    main()