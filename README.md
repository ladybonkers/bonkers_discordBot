<div align="center">

# **Discord bot**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.4+-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 📖 About :

I developed this bot to automate services, similar to a webhook.:

- **Ticket** with manual/scripted workflows;
- **Price list** navigable by category;
- **Store Ryules, terms and information**;
- **Personalized Welcome** for new members.

---

## ✨ Features

### 🎫 Ticket
- Panel with button to open a ticket;
- Choice betwee too types of service **Manual** or **Script**;
- Selection of **category** and **specific service**;
- Automatic private channel creation;
- **Claim Ticket Button** for staff;
- **Automatic notification** in the staff channel;
- Close button on the ticket, just staff members can close.

### 💵 Price List
- Interactive menu with a selection dropdown
- 16 categories about genshin impact
- Individual user view (ephemeral)

### 📢 Commands (using like a webhook)
- `!regras` — Server rules
- `!sobre` — Team informations
- `!termos` — Terms of service
- `!compras` — Buying guide
- `!precos` — Price list
- `!impulsos` — Booster benefits
- `!divulgador` — Promotion program
- `!feedback` — Feedback channel
- `!painel` — Ticket panel

## How to run!

### Pré-requisitos
- **Python 3.9+**
- Create a application on [Discord Developer Portal](https://discord.com/developers/applications)

### 1. Clone the repository

```bash
git clone https://github.com/yourUser/traveler-store-bot.git
cd traveler-store-bot
```

### 2. I recommend to create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create and Configure `.env`

Fill it in with your actual values ​​(token, channel IDs, roles, etc.).

### 5. Run the app

```bash
python3 main.py
```

---

## ⚙️ Config

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
| `DONA_LUMINE_ID` | Lumine's ID (for mentions) |
| `DONA_AETHER_ID` | Aether ID (mention) |
| `WEBHOOK_ID` | Optional external logging webhook | 

### Required bot permissions

Discord Developer Portal → OAuth2 → URL Generator, select:

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

## 📁 Project structure

```
traveler-store-bot/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env.example               # .env template
├── .gitignore                 # Git-ignored files
├── README.md                  # This file
│
├── cogs/                      # Commands and events
│   ├── __init__.py
│   ├── boas_vindas.py         # Welcome messages
│   ├── compras.py             # Shopping guide
│   ├── divulgador.py          # Promotion program
│   ├── feedback.py            # Feedback
│   ├── impulsos.py            # Server boosts
│   ├── precos.py              # Price list
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
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — Enviroment variables

---

## 🧪 Main commands

| Command | Permission | Description |
|---|---|---|
| `!painel` | Manage Server | Posts the ticket panel |
| `!preços` | Manage Server | Posts the price list |
| `!regras` | Manage Server | Posts the rules |
| `!sobre` | Manage Server | Posts the team introduction |
| `!termos` | Manage Server | Posts the terms of service |
| `!compras` | Manage Server | Posts the buying guide |
| `!impulsos` | Manage Server | Posts the server boosts info |
| `!divulgador` | Manage Server | Posts the promotion program |
| `!feedback` | Manage Server | Posts the feedback channel |

---

## 🔒 Security

- **Never** upload the `.env` file to GitHub — it contains the bot token, if the token leaks, **regenerate it immediately** in the Developer Portal;
- If you want to upload for a exemple, recommend using something like: `.env.example` as a template (without real values) for other devs.

---

## 📄 License

This project is for the private use. All rights reserved © (Júlia) LadyBonkers

---

<div align="center">

Made by LadyBonkers

</div>