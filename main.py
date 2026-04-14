import asyncio
import sqlite3
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- SOZLAMALAR ---
# O'z tokeningiz va ID raqamingizni bu yerga yozing
API_TOKEN = '8784362476:AAHOZoukF6o0d9eWLSZoQZT6qBDLxefHAL8' 
ADMIN_ID = 6790315482

# Loglarni yoqish (xatolarni ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlarini yaratish
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Ma'lumotlar bazasini yaratish funksiyasi
def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS movies (name TEXT PRIMARY KEY, file_id TEXT)')
    conn.commit()
    conn.close()

# Start buyrug'i uchun handler
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎬 Salom! Kino nomini yozing, men darhol topib beraman.")

# 1. KANALGA TASHALGAN VIDEONI AVTOMATIK TUTIB OLISH
@dp.channel_post(F.video)
async def auto_save_from_channel(message: types.Message):
    if message.caption:
        # Birinchi qatorni tozalab nom qilib olamiz
        first_line = message.caption.split('\n')[0].lower().strip()
        # Matndagi ortiqcha belgilarni tozalash (emoji yoki "Nomi:" kabi so'zlar)
        movie_name = first_line.replace("film nomi:", "").replace("nomi:", "").replace("🎬", "").strip()
        
        file_id = message.video.file_id
        
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO movies VALUES (?, ?)', (movie_name, file_id))
        conn.commit()
        conn.close()
        print(f"✅ Yangi kino bazaga qo'shildi: {movie_name}")

# 2. FOYDALANUVCHI QIDIRGANDA (Botning o'ziga yozganda)
@dp.message()
async def search_movie(message: types.Message):
    if not message.text: return
    
    query = message.text.lower().strip()
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    # Bazadan qisman o'xshashlik bo'yicha qidirish
    cursor.execute('SELECT file_id FROM movies WHERE name LIKE ?', (f'%{query}%',))
    result = cursor.fetchone()
    conn.close()

    if result:
        await message.answer_video(video=result[0], caption="Marhamat, so'ralgan kino!")
    else:
        await message.answer("🔍 Kechirasiz, bunday kino bazamizda topilmadi.")

# Botni ishga tushirish funksiyasi
async def main():
    init_db()
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")