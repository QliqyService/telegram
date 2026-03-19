# Qliqy Telegram Service

![CI](https://github.com/ilia2003/Qliqy/actions/workflows/telegram-build.yml/badge.svg)
![Status](https://img.shields.io/badge/status-active%20development-b4492f)

Telegram integration service for Qliqy.

## What It Does

- runs the Telegram bot
- links Telegram accounts to Qliqy users via a personal linking code
- receives notification events from `webapi` through RabbitMQ
- sends Telegram messages when new comments arrive

## How It Works

The Telegram bot asks the user for their linking code. That code is sent to `webapi` through RabbitMQ, where the Qliqy account is linked to the Telegram account. After that, comment events published by `webapi` can be delivered to Telegram.

## Product Note

Public registration is intentionally disabled while the platform is still in controlled testing.

Test account:

```json
{
  "email": "admin@admin.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "admin123"
}
```

- Developer: Ilia Fedorenko
- Developer: Ernest Berezin
