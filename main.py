from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# 🔒 ЗАМЕНИ на свои данные
BOT_TOKEN = "7842040350:AAFwJZY_PO4MWRjtgP1t-E08ur39AXlUirc"
MY_TELEGRAM_ID = 1038591016

# Флаг для активации (можно заменить на базу данных, если нужно)
active_users = set()

# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == MY_TELEGRAM_ID:
        active_users.add(user_id)
        await update.message.reply_text("Приступаю к работе.")
    else:
        await update.message.reply_text("Ты не авторизован для активации бота.")

# Обработка всех типов сообщений
async def forward_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if MY_TELEGRAM_ID not in active_users:
        return  # Игнорировать, если /start не вызывали

    message = update.message
    if not message:
        return

    caption = f"[{update.effective_chat.title or 'Private'}] {message.from_user.first_name}"

    if message.text:
        await context.bot.send_message(chat_id=MY_TELEGRAM_ID, text=f"{caption}: {message.text}")
    elif message.voice:
        await context.bot.send_voice(chat_id=MY_TELEGRAM_ID, voice=message.voice.file_id, caption=caption)
    elif message.audio:
        await context.bot.send_audio(chat_id=MY_TELEGRAM_ID, audio=message.audio.file_id, caption=caption)
    elif message.photo:
        await context.bot.send_photo(chat_id=MY_TELEGRAM_ID, photo=message.photo[-1].file_id, caption=message.caption or caption)
    elif message.document:
        await context.bot.send_document(chat_id=MY_TELEGRAM_ID, document=message.document.file_id, caption=caption)
    elif message.video:
        await context.bot.send_video(chat_id=MY_TELEGRAM_ID, video=message.video.file_id, caption=caption)
    else:
        await context.bot.send_message(chat_id=MY_TELEGRAM_ID, text=f"{caption}: [Неподдерживаемый тип сообщения]")

# Запуск приложения
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.ALL, forward_all))

    print("Бот запущен...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
