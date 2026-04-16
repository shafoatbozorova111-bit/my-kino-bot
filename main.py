import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# --- SOZLAMALAR ---
API_TOKEN = '8784362476:AAHOZoukF6o0d9eWLSZoQZT6qBDLxefHAL8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- RENDER UCHUN KICHIK VEB-SERVER ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render bergan portni olamiz yoki 10000 ni ishlatamiz
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server {port} portida ishga tushdi")

# --- BOTNI ISHGA TUSHIRISH ---
async def main():
    # Bir vaqtda ham veb-serverni, ham botni ishga tushiramiz
    asyncio.create_task(start_web_server())
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi")