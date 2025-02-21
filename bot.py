import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode





bot = Bot(token= TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

async def get_crypto_data():
    try:
        # Fetch global market data
        coingecko_url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(coingecko_url).json()

        market_cap = response["data"]["total_market_cap"]["usd"]
        volume_24h = response["data"]["total_volume"]["usd"]
        btc_dominance = response["data"]["market_cap_percentage"]["btc"]

        # Fetch Fear & Greed Index
        fear_greed_url = "https://api.alternative.me/fng/"
        fear_greed = requests.get(fear_greed_url).json()["data"][0]["value"]

        # Fetch Top 10 Crypto Prices
        coins_url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
        coins = requests.get(coins_url, params=params).json()

        prices = "\n".join([f"{coin['name']} (${coin['current_price']})" for coin in coins])

            # دریافت قیمت تتر از Nobitex (در تومان) و تبدیل مقدار به عدد
        nobitex_url = "https://api.nobitex.ir/market/stats"
        nobitex_params = {"srcCurrency": "usdt", "dstCurrency": "rls"}
        nobitex_data = requests.get(nobitex_url, params=nobitex_params).json()

        usdt_to_irt = float(nobitex_data["stats"]["usdt-rls"]["latest"])/10  # ✅ تبدیل مقدار به عدد


        # ایجاد پیام نهایی
        message = f"""
📢 **بروزرسانی وضعیت بازار کریپتو** 🚀

📊 **اطلاعات کلی بازار**:
🟢 **ارزش کل بازار:**  **${market_cap:,.0f}** 💰
🔄 **حجم معاملات ۲۴ ساعته:**  **${volume_24h:,.0f}** 📈
⚡ **تسلط بیت‌کوین:**  **{btc_dominance:.2f}%** 🏆
🧭 **شاخص ترس و طمع:**  **{fear_greed}/100** 😨📊

💎 **۱۰ ارز دیجیتال برتر**:
{prices}

💵 **قیمت تتر (USDT) به تومان**:
💲 **{usdt_to_irt:,.0f} تومان** 🇮🇷

📡 **این اطلاعات هر ۵ دقیقه بروزرسانی می‌شود.**
🔔 *عضو شوید تا اطلاعات لحظه‌ای دریافت کنید!*
"""

        return message

    except Exception as e:
        return f"❌ Error fetching data: {e}"

async def send_crypto_report():
    """Fetch and send crypto market data every 5 minutes."""
    while True:
        message = await get_crypto_data()
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds)

async def main():
    """Start the bot."""
    print("Bot is running...")
    await send_crypto_report()

if __name__ == "__main__":
    asyncio.run(main())
