# OsonFanbot

O‘quv materiallari uchun o‘zbekcha Telegram botning boshlang‘ich versiyasi.
Python, aiogram va SQLite ishlatiladi. Bot uzoq so‘rovlar (`long polling`) orqali
xabarlarni oladi. Ishlashi uchun alohida sayt yoki kiruvchi HTTP porti kerak emas.

## Render’da ishga tushirish

`render.yaml` bitta **Background Worker** va **1 GB doimiy disk** yaratish uchun
tayyorlangan. `Starter` ishchisi va doimiy disk pullik. Yaratishni tasdiqlashdan
oldin Render ko‘rsatgan narxni tekshiring; bu fayllarni GitHub’ga yuborishning
o‘zi xizmat yaratmaydi va to‘lovni boshlamaydi.

1. [Render](https://dashboard.render.com/) saytiga GitHub orqali kiring.
2. **New → Blueprint** ni tanlang. GitHub’dan ruxsat so‘ralsa,
   `rozali020295-gif/OsonFanbot` repository’siga kirishga ruxsat bering.
3. `OsonFanbot` repository’sini va `main` tarmog‘ini tanlang.
   Render repository’dagi `render.yaml` faylini o‘qiydi.
4. So‘ralgan `BOT_TOKEN` maydoniga BotFather bergan tokenni kiriting.
   Tokenni chatga, kodga yoki GitHub fayllariga joylamang.
5. `ADMIN_IDS` qiymati `247126354` qilib tayyorlangan. Bu sizning Telegram
   ID’ingiz bo‘lmasa, Render’da uni almashtiring.
6. Xizmat va disk narxini tekshirib, **Deploy Blueprint** orqali tasdiqlang.
7. Xizmatning **Logs** bo‘limini oching. Xatosiz `Start polling` va
   `Run polling for bot ...` yozuvlari chiqqach, Telegram’da o‘z botingizni ochib,
   `/start` yuboring. O‘zbekcha salomlashuv va menyu chiqishini tekshiring.

GitHub’dagi **Environments** yoki **Actions secrets** qiymatlari Render’ga
avtomatik o‘tmaydi. Tokenni keyin o‘zgartirish uchun Render’dagi xizmatning
**Environment** bo‘limida `BOT_TOKEN` ni yangilang va xizmatni qayta ishga tushiring.

### Qo‘lda xizmat yaratish

Blueprint o‘rniga **New → Background Worker** orqali ham sozlash mumkin:

- Repository: `rozali020295-gif/OsonFanbot`, tarmoq: `main`.
- Ishlash muhiti: **Docker**, Dockerfile: `./Dockerfile`.
- Nusxalar soni: **1**. Bir tokenni bir vaqtning o‘zida boshqa server yoki
  kompyuterda ham polling orqali ishga tushirmang.
- `BOT_TOKEN`: maxfiy token; `ADMIN_IDS`: `247126354`.
- `WEBAPP_URL`: hozircha kiritish shart emas.
- **Disks** bo‘limida 1 GB disk yarating va **Mount path** ni `/app/data` qiling.

Bu kod uchun **Web Service** tanlamang: u HTTP porti ochmaydi.

### Ma’lumotlar va xatolar

SQLite bazasi konteyner ichidagi `/app/data/osonfan.db` fayliga yoziladi.
`render.yaml` aynan `/app/data` papkasini doimiy diskka ulaydi; baza deploy va
qayta ishga tushirishlar orasida saqlanadi. Disk ulanmasa, yangi deploy’da lokal
ma’lumotlar yo‘qolishi mumkin. Disk yoki xizmatni o‘chirishdan oldin bazadan
zaxira nusxa oling.

- `BOT_TOKEN ... kiritilmagan`: Render’dagi **Environment** bo‘limini tekshiring.
- Token yaroqsiz yoki ruxsat rad etilsa: BotFather’dagi amaldagi tokenni Render’da
  yangilang. Tokenni diagnostika uchun chatga yoki logga nusxalamang.
- `Conflict ... getUpdates`: shu token bilan ishlayotgan boshqa bot nusxasini
  to‘xtating va faqat bitta worker qoldiring.
- Baza yozilmasa: diskning **Mount path** qiymati `/app/data` ekanini tekshiring.

## Kompyuterda ishga tushirish

Python 3.12 o‘rnating. Windows PowerShell’da loyiha papkasidan:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` ni matn muharririda ochib, `BOT_TOKEN` va `ADMIN_IDS` ni kiriting.
`WEBAPP_URL` hozircha bo‘sh qolishi mumkin. Keyin:

```powershell
.\.venv\Scripts\python.exe bot.py
```

Linux/macOS’da:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
# .env faylidagi BOT_TOKEN va ADMIN_IDS ni sozlang.
.venv/bin/python bot.py
```

`.env`, virtual muhit va SQLite bazasi `.gitignore` orqali Git’dan chiqarilgan.
Docker tasviriga faqat bot kodi va dependency ro‘yxati ko‘chiriladi; token,
`.env` va lokal baza tasvirga kirmaydi.

## Mini App va mavjud imkoniyatlar

`WEBAPP_URL` bo‘sh bo‘lsa, **Test ishlash** tugmasi bo‘lim tayyorlanayotganini
bildiradi. Boshqa menyular uchun sayt talab qilinmaydi. Mini App ulanadigan
bo‘lsa, haqiqiy HTTPS manzil kerak. `web/` hozircha boshlang‘ich sahifa;
ishlaydigan test tizimi hali tayyor emas. Worker bu papkani internetga chiqarmaydi.

Hozir `/start`, materiallarni ro‘yxatdan olish, material tavsifi, admin ID
tekshiruvi va SQLite asoslari bor. To‘liq material boshqaruvi, qidiruv,
test tizimi, reklama va ommaviy xabar yuborish hali bajarilmagan.
Bot ichida to‘lov qabul qilinmaydi.

## Tekshirish

```bash
.venv/bin/python -m pip check
.venv/bin/python -m unittest discover -s tests -v
docker build -t osonfanbot:local .
```

Ushbu o‘zgarishda 4 ta avtomatik test lokal virtual muhitda va Docker ichida
muvaffaqiyatli o‘tdi. Alohida konteynerlar orasida SQLite bazasining doimiy
diskda saqlanishi ham tekshirildi. Render YAML sintaksisi, worker turi, bitta
nusxa va disk manzilining mosligi tekshirildi.

Mahalliy bulut muhitida Docker tarmog‘i maxsus proxy va uning CA sertifikatini
talab qildi. Docker sinovi vaqtinchalik tashqi Dockerfile nusxasida, faqat pip
bosqichiga mavjud ishonchli CA’ni BuildKit secret orqali ulab bajarildi; TLS
tekshiruvi saqlandi. Bu muhitga xos sertifikat va proxy repository’ga yoki tayyor
tasvirga qo‘shilmadi. Render uchun saqlangan Dockerfile odatiy tarmoqdan foydalanadi.

Asosiy funksional tekshiruv: haqiqiy token bilan worker ishga tushgach,
Telegram’da `/start` va menyu tugmalarini sinab ko‘ring. Haqiqiy Render deploy’i
va Telegram bilan ulanish foydalanuvchi sozlamalari kiritilgandan keyin tekshiriladi.

## Rasmiy manbalar

- [Render Background Workers](https://render.com/docs/background-workers)
- [Render Blueprint spetsifikatsiyasi](https://render.com/docs/blueprint-spec)
- [Render doimiy disklari](https://render.com/docs/disks)
- [Render Docker qo‘llanmasi](https://render.com/docs/docker)
- [Render narxlari](https://render.com/pricing)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- [aiogram](https://docs.aiogram.dev/)
