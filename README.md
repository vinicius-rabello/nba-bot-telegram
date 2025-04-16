# 🤖 NBA Bot Telegram

Este bot permite que qualquer pessoa consulte rapidamente os jogos da NBA que acontecem em uma data específica direto no Telegram.

## 💬 Comandos disponíveis

- `/start` — Mensagem de boas-vindas e ajuda
- `/jogos hoje` — Lista os jogos do dia atual
- `/jogos ontem` — Lista os jogos do dia anterior
- `/jogos amanhã` — Lista os jogos do dia seguinte
- `jogos dia 13` — Consulta para uma data específica (formato flexível)

## 🔌 Integrações

- Os dados são obtidos da API presente em [nba-bot-api](https://github.com/vinicius-rabello/nba-bot-api)
- Os dados são consultados de uma base de dados PostgreSQL hospedada na **Amazon RDS**

## ⚙️ Tecnologias

- Python
- `python-telegram-bot`
- `psycopg2` para acesso à base PostgreSQL
- Hospedado em uma instância EC2 gratuita (free tier)

## 🚀 Deploy

- Roda 24/7 numa instância EC2 (t2.micro) da AWS

## 📎 Exemplo de uso

O usuário envia:

```text
jogos hoje
```

O bot responde:

```text
🏀 Lakers vs Celtics  
🕘 21:30  
📺 ESPN  

🏀 Warriors vs Nets  
🕘 23:00  
📺 NBA League Pass
```

## 🔗 Acesse o bot:

👉 [https://t.me/jogos_nba_bot](https://t.me/jogos_nba_bot)