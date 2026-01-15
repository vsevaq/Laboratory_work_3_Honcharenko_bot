import os
from dotenv import load_dotenv
from threading import Thread

from telegram import Update, ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import openai
from flask import Flask


# ENV
load_dotenv()

TOKENTG = os.getenv("TOKENTG")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


# Клавіатура меню
menu_keyboard = [
    ["Student"],
    ["IT-technologies"],
    ["Contacts"],
    ["Prompt AI"]
]
markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я ваш Telegram-бот\nОберіть пункт меню:",
        reply_markup=markup
    )


def ask_chatgpt(question: str) -> str:
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=question,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("OpenAI API error:", e)
        return "Вибач, не вдалося отримати відповідь від AI."


def menu_handler(update: Update, context: CallbackContext):
    text = update.message.text

    # Перевіряємо команди меню
    if text == "Student":
        update.message.reply_text("ПІБ: Гончаренко В.В.\nГрупа: ІС-з21")
        return
    elif text == "IT-technologies":
        update.message.reply_text("Front-end, Back-end, WEB-технології")
        return
    elif text == "Contacts":
        update.message.reply_text("Тел.: +380501318681\nE-mail: Vsevolodq@gmail.com")
        return
    elif text == "Prompt AI":
        update.message.reply_text("Введіть запит до AI")
        return

    # Все інше йде до OpenAI
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    answer = ask_chatgpt(text)
    update.message.reply_text(answer)



def run_telegram_bot():
    updater = Updater(TOKENTG, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, menu_handler))

    updater.start_polling()
    print("Бот запущено...")

    # це для запуску бота локально у Пайчармі
    #updater.idle()


# FLASK (для Render Web Service)
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)




# Локальний тест Telegram-бота через Пайчарм щоб перевірити що бот працює
# if __name__ == "__main__":
#    run_telegram_bot()


# Для деплою на Render через Web Service
# Запускає Flask, Telegram-бот працює через polling у фоні
# Тут бот запускається у фоні без idle, через Flask Web Service Render
if __name__ == "__main__":
    # запускаємо Telegram-бот у фоновому потоці

    Thread(target=run_telegram_bot).start()

    # запускаємо Flask (Render тримає процес живим)
    run_flask()
