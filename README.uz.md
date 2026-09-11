<div align="center">

[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![Русский](https://img.shields.io/badge/README-Русский-red)](README.ru.md)
[![Oʻzbekcha](https://img.shields.io/badge/README-Oʻzbekcha-green)](README.uz.md)

</div>

# AI Night Watchman

![Namoyish](screenshots/demo.svg)
[![CI](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml/badge.svg)](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml)

Deterministik (LLM ishlatmaydigan) infratuzilma monitoring demoni: Proxmox nodelari, tarmoq kontrollerlari, fayrvollar va xizmatlar. Kritik ogohlantirishlar 5 daqiqa ichida, kunlik digest, haftalik xavfsizlik auditi. Cron vazifalari sifatida ishlaydi — AI model ishdan chiqsa ham davom etadi.

## Nega deterministik?

AI agentlar kuchli, lekin LLM provayderi ishlamayotganda yoki gallyutsinatsiya qilayotganda ishonchsiz. Night Watchman — **sof Python, faqat stdlib** — AI oflayn boʻlsa ham kuzatadi. Bu AI qatlamining ostidagi xavfsizlik toʻri.

## Monitorlar

| Tekshiruv | Interval | Ogohlantirish sharti |
|-----------|----------|----------------------|
| Nodelar erishuvchanligi | 5 daq | API timeout yoki holat ≠ online |
| Saqlash joyi bandligi | 5 daq | > 90% band |
| Qurilmalar holati (tarmoq) | 5 daq | Har qanday qurilma offline/disconnected |
| Shlyuz tirikligi | 5 daq | API erishib boʻlmaydi yoki autentifikatsiya xatosi |
| SSH brute-force | haftada bir | > 20 muvaffaqiyatsiz urinish/hafta |
| Paket yangilanishlari | haftada bir | > 100 kutilmoqda |
| Backup yangiqligi | haftada bir | Yaqindagi backup fayllari yoʻq |
| Port anomaliyalari | haftada bir | Tinglanayotgan portlar soni oʻzgargan |

## Arxitektura

```
┌────────────┐    5 min    ┌──────────────┐    Telegram
│   cron     │──▶│ nightwatch.py│────────▶ │  alerts  │
└────────────┘             └──────────────┘           │
┌────────────┐   weekly    ┌──────────────┐           │
│   cron     │──▶│  secaudit.py │────────▶ │  report │
└────────────┘             └──────────────┘           ▼
```

## Asosiy dizayn qarorlari

1. **Faqat stdlib** — pip bogʻliqliklari yoʻq, har qanday Python 3.10+ da ishlaydi
2. **Deduplikatsiya uchun holat fayli** — ogohlantirishlar har soʻrovda emas, holat oʻzgarganda bir marta ishga tushadi
3. **Ikki chiqish rejimi**: `critical` (faqat yangi/yopilgan ogohlantirishlar) va `digest` (toʻliq xulosa)
4. **Cron + --no-agent** — skript stdout-i toʻgʻridan-toʻgʻri Telegram-ga boradi, zanjirda LLM yoʻq

## Foydalanish

```bash
# Kritik ogohlantirishlar (cron orqali har 5 daqiqada)
./scripts/nightwatch.py critical

# Kunlik digest (cron orqali 08:00 da)
./scripts/nightwatch.py digest

# Haftalik xavfsizlik auditi (dushanba 09:00)
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
