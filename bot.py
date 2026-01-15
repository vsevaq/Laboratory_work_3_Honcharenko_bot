import os

from dotenv import load_dotenv
import openai

from telegram import Update, ReplyKeyboardMarkup, ChatAction
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    Filters
)



load_dotenv()


# Токени

TOKENTG = os.getenv("TOKENTG")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Ініціалізація OpenAI
openai.api_key = OPENAI_API_KEY

# Клавіатура меню
menu_keyboard = [
    ["Student"],
    ["IT-technologies"],
    ["Contacts"],
    ["Prompt AI"]
]
markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я ваш бот. Оберіть опцію з меню нижче:",
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
        return "Вибач, я не зміг отримати відповідь від ChatGPT."



def menu_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Student":
        update.message.reply_text("Прізвище: Гончаренко В.В.\nГрупа: ІС-з21")
    elif text == "IT-technologies":
        update.message.reply_text("Front-ebd, Back-end, WEB-технології")
    elif text == "Contacts":
        update.message.reply_text("Тел.: +380501318681\nE-mail: Vsevolodq@gmail.com")
    elif text == "Prompt AI":
        update.message.reply_text("Введіть свій запит до ChatGPT")
    else:
        # Відправка запиту до ChatGPT
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        answer = ask_chatgpt(text)
        update.message.reply_text(answer)


def main():
    updater = Updater(TOKENTG, use_context=True)
    dispatcher = updater.dispatcher

    # Команди
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), menu_handler))

    # Запуск
    print("Бот запущено...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
