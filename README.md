# Discord Bot — Traveler Store

**A Python bot built with discord.py to automate a Genshin Impact service store.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.4+-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/ladybonkers/bonkers_discordbot?style=for-the-badge&color=8A2BE2)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)

---

## 📖 About

This bot was developed to automate a Genshin Impact service store — handling everything from welcoming new members to managing a complete ticket system with separate pricing for **Manual** and **Script** services.

### ✨ Features

#### 🎫 Ticket System
- Panel with a button to open a ticket
- Choice between two service types: **Manual** or **Script**
- Category and specific service selection (with prices pulled from the right table)
- Automatic private channel creation
- **Claim Ticket** button for staff (with automatic DM notifications to owners)
- Automatic notification in the staff channel with the **discounted price** for farmers
- Close button restricted to staff members
- Add-member modal for including other staff in the ticket

#### 💵 Price List
- Interactive menu with a dropdown
- **Two separate price tables** (Manual & Script)
- 16 categories focused on Genshin Impact services
- Ephemeral view — each user sees only their own selection
- Support for sub-groups (e.g. "Exploration below 50%" / "above 50%")

#### 📢 Information Commands
- Server rules
- Team introduction
- Terms of service
- Buying guide
- Booster benefits
- Promotion program
- Feedback channel
- Welcome messages for new members

---

## 🚀 How to Run

### Prerequisites
- **Python 3.9+**
- A bot application on the [Discord Developer Portal](https://discord.com/developers/applications)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/traveler-store-bot.git
cd traveler-store-bot
```

### 2. (Recommended) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the `.env`

Copy the template and fill it with your real values:

```bash
cp .env.example .env
```

### 5. Run the bot

```bash
python3 main.py
```

---

## ⚙️ Configuration

### Environment variables (`.env`)

| Variable | Description |
|---|---|
| `DISCORD_TOKEN` | Bot token (get it from the Developer Portal) |
| `CANAL_BOAS_VINDAS_ID` | Welcome channel ID |
| `CANAL_LOGS_ID` | Bot logs channel ID |
| `CATEGORIA_TICKETS_ID` | Default ticket category (fallback) |
| `CARGO_STAFF_ID` | Staff role ID (fallback) |
| `CATEGORIA_MANUAL_ID` | Manual ticket category ID |
| `CATEGORIA_SCRIPT_ID` | Script ticket category ID |
| `CARGO_MANUAL_ID` | Manual farmer role ID |
| `CARGO_SCRIPT_ID` | Script farmer role ID |
| `CANAL_NOTIF_MANUAL_ID` | Manual order notification channel ID |
| `CANAL_NOTIF_SCRIPT_ID` | Script order notification channel ID |
| `CARGO_FARMER_ID` | Role mentioned in the notification |
| `DONA_LUMINE_ID` | Lumine's user ID (for mentions and DM notifications) |
| `DONA_AETHER_ID` | Aether's user ID (for mentions and DM notifications) |
| `LOGSTICKET_ID` | Fallback channel for ticket logs if owner DMs are closed |
| `WEBHOOK_ID` | Optional external logging webhook |

### Required bot permissions

In the Discord Developer Portal → OAuth2 → URL Generator, select:

**Scopes:**
- `bot`
- `applications.commands`

**Bot Permissions:**
- ✅ Manage Channels
- ✅ Manage Roles
- ✅ Send Messages
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Message History
- ✅ Manage Messages
- ✅ Use External Emojis
- ✅ Mention Everyone (if using role mentions)

---

## 📁 Project Structure

```
traveler-store-bot/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env.example               # .env template (safe to commit)
├── .gitignore                 # Git-ignored files
├── README.md                  # This file
│
├── banners/                   # Local images used in embeds
│   └── boasvindas.jpeg
│
├── cogs/                      # Commands and events
│   ├── __init__.py
│   ├── boas_vindas.py         # Welcome messages
│   ├── compras.py             # Buying guide
│   ├── divulgador.py          # Promotion program
│   ├── feedback.py            # Feedback channel
│   ├── impulsos.py            # Server boosts
│   ├── precos.py              # Price list (Manual + Script)
│   ├── regras.py              # Rules
│   ├── sobre.py               # About the team
│   ├── termos.py              # Terms of service
│   └── tickets.py             # Ticket system
│
├── utils/                     # Shared helpers
│   ├── __init__.py
│   └── views.py               # Embed helpers
│
└── data/                      # Local data (ignored by git)
```

---

## 🎨 Stack

- **[discord.py](https://github.com/Rapptz/discord.py)** — Main library
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — Environment variables

---

## 🧪 Main Commands

| Command | Permission | Description |
|---|---|---|
| `!painel` | Manage Server | Posts the ticket panel |
| `!precos` | Manage Server | Posts the price list |
| `!regras` | Manage Server | Posts the server rules |
| `!sobre` | Manage Server | Posts the team introduction |
| `!termos` | Manage Server | Posts the terms of service |
| `!compras` | Manage Server | Posts the buying guide |
| `!impulsos` | Manage Server | Posts the server boosts info |
| `!divulgador` | Manage Server | Posts the promotion program |
| `!feedback` | Manage Server | Posts the feedback channel |
| `!add @member` | Staff | Adds a member to the current ticket |
| `!pedidomanual` | Staff | Sends the current manual order to the farmers' channel |
| `!pedidoscript` | Staff | Sends the current script order to the farmers' channel |

---

## 🔒 Security

- **Never upload the `.env` file to GitHub** — it contains the bot token.
- If the token leaks, **regenerate it immediately** in the Developer Portal.
- Use `.env.example` as a template (without real values) for other developers.
- The `data/` folder (if used for caching) is ignored by git.

---

## 📄 License

This project is for **private use**. All rights reserved © (Júlia) LadyBonkers.

---

<div align="center">

**✦ 𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆 ✦**

*Onde sua jornada por Teyvat começa.* 🌙

Made with 💜 by **LadyBonkers**

</div>