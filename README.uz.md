<div align="center">

[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![Русский](https://img.shields.io/badge/README-Русский-red)](README.ru.md)
[![Oʻzbekcha](https://img.shields.io/badge/README-Oʻzbekcha-green)](README.uz.md)

</div>

# AI Night Watchman

![Namoyish](screenshots/demo.svg)
[![CI](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml/badge.svg)](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml)

LLM ishlatmaydigan deterministik monitoring demoni: Proxmox nodelari, tarmoq kontrollerlari, fayrvollar va xizmatlar doimiy kuzatiladi. Kritik ogohlantirishlar 5 daqiqadan kechikmay keladi, har kuni digest, har hafta xavfsizlik auditi. Cron vazifalari sifatida ishlaydi — AI model ishdan chiqsa ham monitoring toʻxtamaydi.

## Nega deterministik?

AI agentlar kuchli, lekin LLM provayderi ishlamay qolsa yoki gallyutsinatsiya qila boshlasa, ularga ishonib boʻlmaydi. Night Watchman esa — sof Python, faqat stdlib: AI oflayn boʻlganda ham kuzatishni davom ettiradi. Oddiy qilib aytganda, bu AI qatlamining ostida turgan orqa himoya qatlami.

## Monitorlar

| Tekshiruv | Interval | Ogohlantirish sharti |
|-----------|----------|----------------------|
| Node holati | 5 daq | API javob bermasa yoki holat online boʻlmasa |
| Saqlash joyi bandligi | 5 daq | 90% dan ortiq band |
| Tarmoq qurilmalari holati | 5 daq | Kamida bitta qurilma offline/disconnected |
| Shlyuz jonliligi | 5 daq | API javob bermasa yoki autentifikatsiya xatosi |
| SSH brute-force | haftalik | Haftada 20 dan ortiq muvaffaqiyatsiz urinish |
| Paket yangilanishlari | haftalik | 100 dan ortiq yangilanish kutilmoqda |
| Backup yangiqligi | haftalik | Yaqin orada backup fayllari tushmagan |
| Port anomaliyalari | haftalik | Tinglanayotgan portlar soni oʻzgargan |

## Arxitektura

```
┌────────────┐    5 min    ┌──────────────┐    Telegram
│   cron     │──▶│ nightwatch.py│────────▶ │  alerts  │
└────────────┘             └──────────────┘           │
┌────────────┐   weekly    ┌──────────────┐           │
│   cron     │──▶│  secaudit.py │────────▶ │  report │
└────────────┘             └──────────────┘           ▼
```

## Dizayn boʻyicha asosiy qarorlar

1. **Faqat stdlib** — pip bogʻliqliklari umuman yoʻq, Python 3.10+ oʻrnatilgan har qanday tizimda ishlaydi
2. **Deduplikatsiya uchun holat fayli** — ogohlantirish har soʻrovda emas, faqat holat oʻzgarganda yuboriladi
3. **Ikki chiqish rejimi**: `critical` (faqat yangi va yopilgan ogohlantirishlar) hamda `digest` (toʻliq xulosa)
4. **Cron + --no-agent** — skript natijasi toʻgʻridan-toʻgʻri Telegram-ga tushadi, zanjirda LLM umuman ishtirok etmaydi

## Foydalanish

```bash
# Kritik ogohlantirishlar (cron bilan har 5 daqiqada)
./scripts/nightwatch.py critical

# Kunlik digest (cron bilan soat 08:00 da)
./scripts/nightwatch.py digest

# Haftalik xavfsizlik auditi (dushanba soat 09:00)
./scripts/secaudit.py
```

## Litsenziya
MIT

## 📬 Aloqa

Savollaringiz bormi? Yozing: **[allumaxmail@gmail.com](mailto:allumaxmail@gmail.com)**

---

<div align="center">

[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![Русский](https://img.shields.io/badge/README-Русский-red)](README.ru.md)
[![Oʻzbekcha](https://img.shields.io/badge/README-Oʻzbekcha-green)](README.uz.md)

</div>
