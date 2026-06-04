import asyncio
import random
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "8950755352:AAHmmg0TVsG0KRZ2OBVPETCArpHsOp1Xgpc"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------------- START ----------------
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Привет! Я бот помощник.\n\n"
        "Напиши /help чтобы увидеть команды."
    )

# ---------------- HELP ----------------
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "📌 Команды:\n"
        "/start - запуск\n"
        "/help - помощь\n"
        "/about - о боте\n"
        "/random - случайное число\n"
        "/calc 2+2 - калькулятор\n"
        "/weather Astana - погода\n"
        "/fact - случайный факт\n"
    )

# ---------------- ABOUT ----------------
@dp.message(Command("about"))
async def about(message: Message):
    await message.answer("🤖 Я учебный Telegram-бот на Python (aiogram).")

# ---------------- RANDOM ----------------
@dp.message(Command("random"))
async def random_cmd(message: Message):
    await message.answer(f"🎲 Случайное число: {random.randint(1, 100)}")

# ---------------- CALC ----------------
@dp.message(Command("calc"))
async def calc(message: Message):
    try:
        expression = message.text.replace("/calc", "").strip()
        result = eval(expression)
        await message.answer(f"🧮 Результат: {result}")
    except:
        await message.answer("❌ Ошибка в выражении")

# ---------------- WEATHER ----------------
@dp.message(Command("weather"))
async def weather(message: Message):
    city = message.text.replace("/weather", "").strip()

    if not city:
        await message.answer("Напиши город: /weather Astana")
        return

    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url).text
        await message.answer(f"🌤 {response}")
    except:
        await message.answer("❌ Не удалось получить погоду")

# ---------------- FACT ----------------
@dp.message(Command("fact"))
async def fact(message: Message):
    try:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url).json()

        fact_text = response["text"]

        await message.answer(f"📌 Случайный факт:\n\n{fact_text}")

    except:
        await message.answer("❌ Ошибка получения факта")

# ---------------- TEXT HANDLER ----------------
@dp.message()
async def text_handler(message: Message):
    text = message.text.lower()

    # привет
    if text == "привет":
        await message.answer("👋 Привет!")
        return

    # число обработка
    if text.isdigit() or (text.startswith("-") and text[1:].isdigit()):
        num = int(text)

        parity = "чётное" if num % 2 == 0 else "нечётное"

        if num > 0:
            sign = "положительное"
        elif num < 0:
            sign = "отрицательное"
        else:
            sign = "ноль"

        await message.answer(
            f"🔢 {num}\n➡ {parity}\n➡ {sign}"
        )
        return

    await message.answer("❓ Не понял команду. Напиши /help")

# ---------------- MAIN ----------------
async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())