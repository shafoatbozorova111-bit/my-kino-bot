import os
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# --- SOZLAMALAR ---
# Tokenni o'zingizniki bilan almashtiring
API_TOKEN = '8784362476:AAHOZoukF6o0d9eWLSZoQZT6qBDLxefHAL8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- BAZA BILAN ISHLASH ---
def search_movie_in_db(movie_name):
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        # Nomi bo'yicha qidirish (LIKE orqali qisman o'xshashlikni ham topadi)
        # Agar sizda ustun nomi 'name' bo'lsa, 'caption'ni 'name'ga almashtiring
        cursor.execute("""
            SELECT file_id, caption FROM movies 
            WHERE caption LIKE ?
        """, (f'%{movie_name}%',))
        
        result = cursor.fetchone()
        conn.close()
        return result # (file_id, caption) qaytaradi
    except Exception as e:
        print(f"Baza xatosi: {e}")
        return None

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Menga kino nomini yuboring, men uni topib beraman. 🎬")

@dp.message(F.text)
async def handle_movie_search(message: types.Message):
    movie_name = message.text.strip()
    
    # Bazadan qidirish
    data = search_movie_in_db(movie_name)
    
    if data:
        file_id, caption = data
        await bot.send_video(
            chat_id=message.chat.id,
            video=file_id,
            caption=f"🎬 **Topilgan kino:** {caption}\n\nDo'stlarga ham ulashing!",
            parse_mode="Markdown"
        )
    else:
        await message.answer(f"❌ Afsuski, '{movie_name}' nomli kino topilmadi.")

# --- RENDER UCHUN VEB-SERVER (O'CHIRMANG!) ---
async def handle(request):
    return web.Response(text="Kino Bot is live on Render!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render avtomatik beradigan PORT yoki 10000
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server {port}-portda ishga tushdi")

# --- ASOSIY ISHGA TUSHIRISH ---
async def main():
    # Veb-serverni orqa fonda (task sifatida) ishga tushiramiz
    asyncio.create_task(start_web_server())
    
    print("Bot pollingni boshladi...")
    # Eski xabarlarni o'chirib yuborish (ixtiyoriy)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi")