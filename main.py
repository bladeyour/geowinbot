
import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", 7023982389:AAEwMMLQZZM3uJu-XoZK9ejur-H52FtO_XQ")
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

def get_user(chat_id):
    if chat_id not in user_data:
        user_data[chat_id] = {"deposit": 0, "win": 0, "loss": 0}
    return user_data[chat_id]

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я GeoWinBot 🎰

Команди:
/депозит <сума>
/виграш <сума>
/злив <сума>
/баланс
/статистика")

@bot.message_handler(commands=["депозит"])
def set_deposit(message):
    try:
        amount = float(message.text.split()[1])
        user = get_user(message.chat.id)
        user["deposit"] += amount
        bot.reply_to(message, f"✅ Депозит додано: {amount} грн")
    except:
        bot.reply_to(message, "❌ Невірний формат. Введи так: /депозит 1500")

@bot.message_handler(commands=["виграш"])
def add_win(message):
    try:
        amount = float(message.text.split()[1])
        user = get_user(message.chat.id)
        user["win"] += amount
        bot.reply_to(message, f"💰 Виграш додано: {amount} грн")
    except:
        bot.reply_to(message, "❌ Невірний формат. Введи так: /виграш 2500")

@bot.message_handler(commands=["злив"])
def add_loss(message):
    try:
        amount = float(message.text.split()[1])
        user = get_user(message.chat.id)
        user["loss"] += amount
        bot.reply_to(message, f"📉 Злив додано: {amount} грн")
    except:
        bot.reply_to(message, "❌ Невірний формат. Введи так: /злив 800")

@bot.message_handler(commands=["баланс"])
def show_balance(message):
    user = get_user(message.chat.id)
    balance = user["deposit"] + user["win"] - user["loss"]
    bot.reply_to(message, f"💼 Поточний баланс: {balance:.2f} грн")

@bot.message_handler(commands=["статистика"])
def show_stats(message):
    user = get_user(message.chat.id)
    balance = user["deposit"] + user["win"] - user["loss"]
    profit = balance - user["deposit"]
    percent = (profit / user["deposit"] * 100) if user["deposit"] > 0 else 0
    bot.reply_to(message, f"📊 Статистика:
Депозит: {user['deposit']} грн
Виграш: {user['win']} грн
Злив: {user['loss']} грн
Баланс: {balance:.2f} грн
Зміна: {profit:.2f} грн ({percent:.1f}%)")

print("Bot is running...")
bot.polling()
