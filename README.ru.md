<div align="center">

[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![Русский](https://img.shields.io/badge/README-Русский-red)](README.ru.md)
[![Oʻzbekcha](https://img.shields.io/badge/README-Oʻzbekcha-green)](README.uz.md)

</div>

# AI Night Watchman

![Демонстрация](screenshots/demo.svg)
[![CI](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml/badge.svg)](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml)

Детерминированный (без LLM) демон мониторинга инфраструктуры: ноды Proxmox, сетевые контроллеры, файрволы и сервисы. Критические алерты в течение 5 минут, ежедневный дайджест, еженедельный аудит безопасности. Работает как cron-задачи — переживает сбои AI-моделей.

## Почему детерминированный?

AI-агенты мощны, но ненадёжны, когда провайдер LLM недоступен или галлюцинирует. Night Watchman — **чистый Python, только stdlib** — он мониторит, даже когда AI офлайн. Это страховочная сетка под AI-слоем.

## Мониторы

| Проверка | Интервал | Условие алерта |
|----------|----------|----------------|
| Доступность нод | 5 мин | Таймаут API или статус ≠ online |
| Заполненность хранилищ | 5 мин | > 90% занято |
| Состояния устройств (сеть) | 5 мин | Любое устройство offline/disconnected |
| Живость шлюза | 5 мин | API недоступен или ошибка аутентификации |
| SSH brute-force | раз в неделю | > 20 неудачных попыток/неделю |
| Обновления пакетов | раз в неделю | > 100 ожидающих |
| Свежесть бэкапов | раз в неделю | Нет недавних файлов бэкапов |
| Аномалии портов | раз в неделю | Изменилось число слушающих портов |

## Архитектура

```
┌────────────┐    5 min    ┌──────────────┐    Telegram
│   cron     │──▶│ nightwatch.py│────────▶ │  alerts  │
└────────────┘             └──────────────┘           │
┌────────────┐   weekly    ┌──────────────┐           │
│   cron     │──▶│  secaudit.py │────────▶ │  report │
└────────────┘             └──────────────┘           ▼
```

## Ключевые проектные решения

1. **Только stdlib** — нет pip-зависимостей, работает на любом Python 3.10+
2. **Файл состояния для дедупликации** — алерты срабатывают один раз при смене состояния, а не при каждом опросе
3. **Два режима вывода**: `critical` (только новые/закрытые алерты) и `digest` (полная сводка)
4. **Cron + --no-agent** — stdout скрипта идёт напрямую в Telegram, без LLM в цепочке

## Использование

```bash
# Критические алерты (каждые 5 минут через cron)
./scripts/nightwatch.py critical

# Ежедневный дайджест (08:00 через cron)
./scripts/nightwatch.py digest

# Еженедельный аудит безопасности (понедельник 09:00)
./scripts/secaudit.py
```

## Лицензия
MIT

## 📬 Контакты

Вопросы? Пишите: **[allumaxmail@gmail.com](mailto:allumaxmail@gmail.com)**

---

<div align="center">

[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![Русский](https://img.shields.io/badge/README-Русский-red)](README.ru.md)
[![Oʻzbekcha](https://img.shields.io/badge/README-Oʻzbekcha-green)](README.uz.md)

</div>
