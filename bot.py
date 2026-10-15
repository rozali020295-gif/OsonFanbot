import asyncio
import logging
import os
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from dotenv import load_dotenv

load_dotenv()
BASE = Path(__file__).parent
DB = BASE / "data" / "osonfan.db"
DB.parent.mkdir(exist_ok=True)
TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMINS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()}
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript("""
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, joined_at TEXT DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS materials (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT DEFAULT '', category TEXT DEFAULT 'Boshqa', kind TEXT DEFAULT 'free', file_id TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
    """)
    return con

def menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔎 Material qidirish"), KeyboardButton(text="📚 Kategoriyalar")],
        [KeyboardButton(text="🆓 Bepul materiallar"), KeyboardButton(text="💎 Pulli materiallar")],
        [KeyboardButton(text="📝 Test ishlash"), KeyboardButton(text="🆕 Yangi materiallar")],
        [KeyboardButton(text="❓ Yordam")],
        [KeyboardButton(text="📢 @att_testlar"), KeyboardButton(text="📢 @infoedu_uz")],
    ], resize_keyboard=True)

def material_buttons(rows):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=r["title"], callback_data=f"mat:{r['id']}")] for r in rows])

dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    with db() as con:
        con.execute("INSERT OR IGNORE INTO users(id, username) VALUES (?, ?)", (message.from_user.id, message.from_user.username))
    await message.answer("Assalomu alaykum! OsonFan botiga xush kelibsiz.\n\nSizga nima kerak?", reply_markup=menu())

@dp.message(F.text == "🆓 Bepul materiallar")
async def free_materials(message: types.Message):
    with db() as con: rows = con.execute("SELECT * FROM materials WHERE kind='free' ORDER BY id DESC LIMIT 30").fetchall()
    await message.answer("Bepul materiallar:" if rows else "Hozircha bepul materiallar qo‘shilmagan.", reply_markup=material_buttons(rows) if rows else None)

@dp.message(F.text == "💎 Pulli materiallar")
async def paid_materials(message: types.Message):
    with db() as con: rows = con.execute("SELECT * FROM materials WHERE kind='paid' ORDER BY id DESC LIMIT 30").fetchall()
    await message.answer("Pulli materiallar. To‘liq nusxa uchun @rozali95 ga yozing:" if rows else "Hozircha pulli materiallar qo‘shilmagan.", reply_markup=material_buttons(rows) if rows else None)

@dp.message(F.text == "📚 Kategoriyalar")
async def categories(message: types.Message):
    await message.answer("Kategoriyalar:\n• Informatika\n• Matematika\n• Fizika\n• Testlar\n• Dars ishlanmalari\n• Boshqa materiallar")

@dp.message(F.text == "🆕 Yangi materiallar")
async def newest(message: types.Message):
    with db() as con: rows = con.execute("SELECT * FROM materials ORDER BY id DESC LIMIT 10").fetchall()
    await message.answer("Yangi materiallar:" if rows else "Hozircha materiallar yo‘q.", reply_markup=material_buttons(rows) if rows else None)

@dp.message(F.text == "📝 Test ishlash")
async def tests(message: types.Message):
    url = urlsplit(WEBAPP_URL)
    if url.scheme != "https" or not url.netloc:
        await message.answer("Testlar bo‘limi hozircha tayyorlanmoqda. Boshqa bo‘limlardan foydalanishingiz mumkin.")
        return
    await message.answer("Testlar bo‘limi Mini App orqali ishlaydi.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📝 Mini Appni ochish", web_app=WebAppInfo(url=WEBAPP_URL))]]))

@dp.message(F.text == "❓ Yordam")
async def help_message(message: types.Message):
    await message.answer("Material izlash uchun menyudan foydalaning. Pulli materialning to‘liq nusxasi uchun @rozali95 ga murojaat qiling.")

@dp.message(F.text.startswith("/admin"))
async def admin(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Sizda admin huquqi yo‘q."); return
    await message.answer("Admin paneli:\n/admin_stats — statistika\n/admin_add Nomi | Tavsif | bepul yoki pulli — material qo‘shish")

@dp.message(F.text.startswith("/admin_stats"))
async def stats(message: types.Message):
    if message.from_user.id not in ADMINS: return
    with db() as con:
        users = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]; mats = con.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    await message.answer(f"Foydalanuvchilar: {users}\nMateriallar: {mats}")

@dp.callback_query(F.data.startswith("mat:"))
async def material(callback: types.CallbackQuery):
    mid = callback.data.split(":", 1)[1]
    with db() as con: row = con.execute("SELECT * FROM materials WHERE id=?", (mid,)).fetchone()
    if not row: await callback.answer("Material topilmadi.", show_alert=True); return
    text = f"<b>{row['title']}</b>\n\n{row['description']}"
    if row["kind"] == "paid": text += "\n\nTo‘liq nusxa uchun @rozali95 ga yozing."
    await callback.message.answer(text, parse_mode="HTML"); await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not TOKEN: raise RuntimeError("BOT_TOKEN environment o‘zgaruvchisi kiritilmagan")
    await dp.start_polling(Bot(TOKEN))

if __name__ == "__main__": asyncio.run(main())

