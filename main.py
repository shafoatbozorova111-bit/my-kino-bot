import os
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# --- SOZLAMALAR ---
API_TOKEN = '8784362476:AAHOZoukF6o0d9eWLSZoQZT6qBDLxefHAL8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- BAZA BILAN ISHLASH ---
def get_movie_data(code):
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        # Jadvalingizda 'file_id' va 'caption' (kino nomi/izohi) bor deb hisoblaymiz
        cursor.execute("SELECT file_id, caption FROM movies WHERE id = ?", (code,))
        result = cursor.fetchone()
        conn.close()
        return result # (file_id, caption) qaytaradi
    except Exception as e:
        print(f"Baza xatosi: {e}")
        return None

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Kino kodini yuboring, men sizga videoni yuboraman! 🎬")

@dp.message(F.text)
async def send_movie_video(message: types.Message):
    code = message.text
    if code.isdigit():
        movie_data = get_movie_data(code)
        
        if movie_data:
            file_id, caption = movie_data
            # Videoni file_id orqali yuborish
            await bot.send_video(
                chat_id=message.chat.id,
                video=file_id,
                caption=f"🎬 {caption}\n\nDo'stlarga ham ulashing!"
            )
        else:
            await message.answer("❌ Afsuski, bu kod bo'yicha kino topilmadi.")
    else:
        await message.answer("Iltimos, kino kodini raqamlarda yuboring.")

# --- RENDER UCHUN VEB-SERVER (O'CHIRMANG!) ---
async def handle(request):
    return web.Response(text="Kino Bot is live!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    asyncio.create_task(start_web_server())
    print("Bot kanaldan video yuborishga tayyor...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())