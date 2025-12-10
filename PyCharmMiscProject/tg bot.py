from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import random
import os

# Картки: назва, рідкість, локальний шлях до зображення
cards = {
    "common": [
        {"name": "Minecraft", "image": "images/common/minecraft.jpg"},
        {"name": "Among Us", "image": "images/common/among_us.jpg"},
        {"name": "Counter Strike 2", "image": "images/common/counterstrike_2.jpg"},
        {"name": "Roblox", "image": "images/common/roblox.jpg"}

    ],
    "rare": [
        {"name": "Cyberpunk 2077", "image": "images/rare/cyberpunk.jpg"},
        {"name": "The Witcher 3", "image": "images/rare/witcher3.jpg"},
        {"name": "Resident Evil 2", "image": "images/rare/residentevil2.jpg"},
        {"name": "Ghostrunner", "image": "images/rare/ghostrunner.jpg"}
    ],
    "epic": [
        {"name": "Elden Ring", "image": "images/epic/elden_ring.jpg"},
        {"name": "God of War", "image": "images/epic/god_of_war.jpg"},
        {"name": "GTA 5", "image": "images/epic/gta 5.jpg"},
        {"name": "Mortal kombat X", "image": "images/epic/mortalkombatx.jpg"},
        {"name": "THE LAST OF US PART 2", "image": "images/epic/The Last OF US Part 2.jpg"}

    ],
    "legends":[
        {"name": "THE LAST OF US", "image": "images/legends/TheLastofUs.jpg"},
        {"name": "Sapper", "image": "images/legends/sapper.png"},
        {"name": "Purple place", "image": "images/legends/purpleplace.jpg"},
        {"name": "Warcraft3", "image": "images/legends/warcraft3.jpg"},
        {"name": "Sudway Surfers", "image": "images/legends/sudwaysurfers.jpg"}
    ]
}

# Функція для створення клавіатури з кнопкою
def get_keyboard():
    keyboard = [[InlineKeyboardButton("Кинути картку гри 🎴", callback_data="draw_card")]]
    return InlineKeyboardMarkup(keyboard)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Вітаю! Натисни кнопку знизу, щоб кинути картку 🎴"
    await update.message.reply_text(text, reply_markup=get_keyboard())

# Обробка кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "draw_card":
        rarity = random.choices(["common", "rare", "epic","legends"], weights=[50, 30, 7, 2])[0]
        card = random.choice(cards[rarity])

        if os.path.exists(card["image"]):
            with open(card["image"], "rb") as photo:
                # Відправляємо картку і одночасно кнопку знову
                await query.message.reply_photo(
                    photo=photo,
                    caption=f"{rarity.capitalize()} картка: {card['name']}",
                    reply_markup=get_keyboard()
                )
        else:
            await query.message.reply_text("Фото не знайдено 😢", reply_markup=get_keyboard())

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token("8515286244:AAHtXd2ro1qry8cORYdH4SaNTZgMbzKhyAE").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

