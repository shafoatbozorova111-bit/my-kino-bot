import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# 1. Avval tokenni yozamiz (probelsiz!)
API_TOKEN = '8784362476:AAHOZoukF6o0d9eWLSZoQZT6qBDLxefHAL8'

# 2. Keyin obyektlarni yaratamiz
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 3. ENDI handlerlarni yozsak bo'ladi (dp endi mavjud)
@dp.message()
async def test_handler(message: types.Message):
    await message.answer("✅ Bot ishlayapti! Siz yozdingiz: " + message.text)

# 4. Qolgan qismlari (veb-server va main)
async def handle(request):
    return web.Response(text="Bot is live!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    print("Bot pollingni boshladi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())