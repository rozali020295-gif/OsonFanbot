# OsonFanbot

O‘zbek tilidagi o‘quv materiallari va testlar Telegram boti.

## Ishga tushirish

1. Python 3.11 yoki undan yangisini o‘rnating.
2. `python -m venv .venv` va Windows’da `.venv\\Scripts\\activate`, Linux/macOS’da `source .venv/bin/activate` buyrug‘ini bajaring.
3. `pip install -r requirements.txt` bajaring.
4. `.env.example` faylidan `.env` yarating va `BOT_TOKEN` hamda `ADMIN_IDS` ni kiriting. Tokenni kodga yozmang va chatga yubormang.
5. `python bot.py` bilan ishga tushiring.

Mini App uchun `web/` katalogini HTTPS domen orqali joylashtiring va `WEBAPP_URL` ga shu manzilni kiriting. Lokal HTTP Telegram’da Mini App sifatida ishlamasligi mumkin.

## Admin

`/admin` va `/admin_stats` faqat `ADMIN_IDS` dagi Telegram ID’lar uchun ishlaydi. Ishlab chiqarish versiyasida material boshqaruvi, moderatsiya, test savollari, reklama statistikasi va ommaviy xabar yuborish funksiyalari alohida admin panelga kengaytiriladi.

## Rasmiy manbalar

- https://core.telegram.org/bots/api
- https://core.telegram.org/bots/webapps
- https://docs.aiogram.dev/

Bot hozircha Telegram ichida to‘lov qabul qilmaydi; pulli materiallar faqat tanishtiriladi va to‘liq nusxa uchun `@rozali95` ga murojaat yo‘naltiriladi.
