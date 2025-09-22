import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession

API_ID = 22731419
API_HASH = "2e2a9ce500a5bd08bae56f6ac2cc4890"
BOT_TOKEN = "7936881674:AAFhO3rBeNLqCka4xDQ3UenJCF8PMpxf1cE"

# ❗❗ Bu yerga o‘zingiz lokalda olgan SESSION STRING ni qo‘ying
SESSION_STRING = "BU YERGA O‘Z SESSION STRINGINGIZNI QO‘YING"

# Guruh va kanal linklari + ID lar
GROUPS = [
    "https://t.me/buvayda_toshkent_bogdod_toshkent",
    "https://t.me/buvayda_toshkentttt",
    "https://t.me/Toshkent_bogdod_buvayda_taksi",
    "https://t.me/buvayda_bogdod_rishton_toshkend1",
    "https://t.me/bagdod_toshkent_t",
    "https://t.me/bagdod_toshkent_buvayda",
    "https://t.me/Buvayda_Bogdod_Toshkent",
    "https://t.me/Toshkent_Rishton",
    "https://t.me/Toshkent_Bogdod_Toshken",
    "https://t.me/Rishton_Buvayda_Toshkent_Bogdod",
    "https://t.me/Toshkent_Bagdod_toshken",
    "https://t.me/toshkenbogdodd",
    "https://t.me/BUVAYDA_YANGIQORGON_Toshkentt",
    "https://t.me/toshkent_buvayda_bagdodd",
    "https://t.me/rishron_toshkent_rishton",
    "https://t.me/bogdod_toshkent_shafyorlar",
    "https://t.me/rishton_toshkent_taksil",
    "https://t.me/rishton_toshkent_bogdod_n1",
    "https://t.me/Rishton_Buvayda_Toshkent_Bogdodi",
    "https://t.me/Vodiy_Toshkent_taxi_xizmatiN1",
    "https://t.me/buvayda_toshkent_buvayda_taxi",
    "https://t.me/Bogdodtoshkenttaksi1",
    "https://t.me/Rishton_bogdodToshkent",
    "https://t.me/toshkent_uyrat_dormancha",
    "https://t.me/buvayda_toshkent_taksi2",
    "https://t.me/Bogdod_toshkent_yangiqorgonbuvay",
    "https://t.me/rishton_toshkent_bogdod_1",
    "https://t.me/toshkent_bogdod_rishton_buvayd",
    "https://t.me/toshkent_bogdod_toshkent_taksi",
    "https://t.me/taxi_bogdod_toshken",
    "https://t.me/toshkent_rishtonn",
    "https://t.me/RishtonBagdodToshkent",
    "https://t.me/bagdod_rishton_qoqon_toshkent",
    "https://t.me/rishton_toshkent_1",
    "https://t.me/Rishton_Toshkent_Rishton",
    "https://t.me/toshkent_rishton_taxi",
    "https://t.me/RishtanTashkent",
    "https://t.me/Rishton_Toshkent2",
    "https://t.me/toshkentrishtonbagdod",
    "https://t.me/bagdod_rishton_toshkent_qoqon",
    "https://t.me/Rishton_Toshkent",
    "https://t.me/taxichen",
    "https://t.me/RishtonToshkenttaxiii",
    "https://t.me/RishtonGa",
    "https://t.me/Toshkent_Fargona_taxis",
    "https://t.me/bagdod_buvayda0",
    "https://t.me/TOSHKENT_RISHTON_TAXI_745",
    "https://t.me/Toshkent_Rishton24",
    "https://t.me/ToshkentRishtonTaxi",
    "https://t.me/pitagkr",
    "https://t.me/Rishton_Toshkent_Bogdod_Taksi_01",
    "https://t.me/rishton_toshkent_24",
    "https://t.me/toshkent_bogdod_buvayda_taxi",
    "https://t.me/rishton_taxi_toshkent",
    "https://t.me/rishton_toshkent_bogdod_1234",
    "https://t.me/rishton_toshkent_bogdod_taxi_12",
    1673082649,
    2257001893,
    1910120507,
    2335396180,
    1373629932
]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

user_data = {}
last_messages = {}

# --- Klaviaturalar ---
def start_menu():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("📤 E'lon berish", callback_data="elon"))

def confirm_menu():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("✅ Tasdiqlash", callback_data="tasdiqla"))

def cancel_reply_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⛔ To‘xtatish"))
    return kb

def new_ad_button():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("📤 Yangi e'lon", callback_data="elon"))

# --- Start ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Assalomu alaykum!\nE'lon yuborish uchun quyidagini tanlang:", reply_markup=start_menu())

# --- Tugmalar ---
@dp.callback_query_handler(lambda call: True)
async def callbacks(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == "elon":
        user_data[user_id] = {"step": "waiting_for_elon", "stop": False}
        await call.message.edit_reply_markup()
        await call.message.answer("✍️ E'lon matnini yuboring:", reply_markup=ReplyKeyboardRemove())

    elif call.data == "tasdiqla":
        if user_id not in user_data or "text" not in user_data[user_id]:
            await call.message.answer("Avval e'lon yuboring.")
            return

        user_data[user_id]["stop"] = False
        await call.message.edit_reply_markup()
        await call.message.answer("📤 E'lon yuborilmoqda...", reply_markup=cancel_reply_button())
        text = user_data[user_id]["text"]

        async def continuous_send():
            while not user_data.get(user_id, {}).get("stop"):
                # Eski xabarlarni o‘chirish
                for group, msg in list(last_messages.items()):
                    try:
                        await client.delete_messages(group, msg.id)
                    except:
                        pass
                last_messages.clear()

                # Yangi yuborish
                for group in GROUPS:
                    if user_data.get(user_id, {}).get("stop"):
                        await bot.send_message(user_id, "❌ Yuborish to‘xtatildi.", reply_markup=new_ad_button())
                        return
                    try:
                        if not client.is_connected():
                            await client.connect()
                        sent = await client.send_message(group, text)
                        last_messages[group] = sent
                        await bot.send_message(user_id, f"✅ Yuborildi: {group}")

                    except FloodWaitError as e:
                        await bot.send_message(user_id, f"⏱ Kutish kerak {e.seconds} sekund ({group})")
                        await asyncio.sleep(e.seconds)

                    except Exception as e:
                        await bot.send_message(user_id, f"❌ Xatolik: {group}\n{e}")

                    await asyncio.sleep(2)  # har bir guruh orasida 2 sek kutish

                await asyncio.sleep(180)  # 3 minut kutib yana yuboradi

        asyncio.create_task(continuous_send())

# --- To‘xtatish tugmasi ---
@dp.message_handler(lambda msg: msg.text == "⛔ To‘xtatish")
async def stop_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data[user_id]["stop"] = True
    await message.answer("🚫 Yuborish to‘xtatildi.", reply_markup=ReplyKeyboardRemove())
    await message.answer("Yuborishni qaytadan boshlash uchun tugmani bosing:", reply_markup=new_ad_button())

# --- Matn qabul qilish ---
@dp.message_handler()
async def text_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_elon":
        user_data[user_id]["text"] = message.text
        user_data[user_id]["step"] = "ready"
        await message.answer("✅ E'lon qabul qilindi. Tasdiqlash uchun tugmani bosing:", reply_markup=confirm_menu())
    else:
        await message.answer("E'lon yuborish uchun /start buyrug‘idan foydalaning.")

# --- Botni ishga tushirish ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await client.start()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
