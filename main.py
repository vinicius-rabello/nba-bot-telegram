from telegram.ext import Application, CommandHandler
from database.db import get_by_date
from utils import format_games_message
from datetime import datetime, timedelta
from config.settings import TELEGRAM_BOT_TOKEN
from pytz import timezone


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

def main():
    print("Starting bot...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('jogos', jogos))

    print("Bot initialized, starting polling...")
    application.run_polling()
    print("Polling started")

if __name__ == '__main__':
    main()