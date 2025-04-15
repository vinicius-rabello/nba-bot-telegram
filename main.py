from telegram.ext import Application, CommandHandler
from database.db import get_by_date
from utils import format_games_message
from datetime import datetime
from config.settings import TELEGRAM_BOT_TOKEN

async def jogos(update, context):
    # Get date from command arguments or use today
    try:
        date = datetime.strptime(context.args[0], '%Y-%m-%d').date()
    except (IndexError, ValueError):
        date = datetime.now().date()
    
    games_data = get_by_date(date)
    message = format_games_message(games_data)
    await update.message.reply_text(message, parse_mode='Markdown')

def main():
    print("Starting bot...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('jogos', jogos))
    print("Bot initialized, starting polling...")
    application.run_polling()
    print("Polling started")

if __name__ == '__main__':
    main()