from __future__ import annotations

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "cogs.boas_vindas",
    "cogs.regras",
    "cogs.sobre",
    "cogs.termos",
    "cogs.compras",
    "cogs.precos",
    "cogs.impulsos",
    "cogs.divulgador",
    "cogs.feedback",
    "cogs.tickets",
]


@bot.event
async def setup_hook():
    # Carrega todos os cogs e registra a view persistente do painel de tickets
    for cog in COGS:
        await bot.load_extension(cog)

    from Bonkers_DiscordBot.projeto.cogs.tickets import PainelTicketView
    bot.add_view(PainelTicketView())


@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

    canal_logs_id = int(os.getenv("CANAL_LOGS_ID", "0"))
    dona_aether = os.getenv("DONA_AETHER_ID", "0")
    canal_logs = bot.get_channel(canal_logs_id)
    if canal_logs:
        await canal_logs.send(
            f"🟢 **{bot.user.name}** está online agora! Vai tomando <@{dona_aether}>"
        )

@bot.event
async def setup_hook():
    for cog in COGS:
        await bot.load_extension(cog)

    from Bonkers_DiscordBot.projeto.cogs.tickets import PainelTicketView, TicketAbertoView
    from Bonkers_DiscordBot.projeto.cogs.precos import MenuPrecosView

    bot.add_view(PainelTicketView())
    bot.add_view(TicketAbertoView())
    bot.add_view(MenuPrecosView())


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Defina DISCORD_TOKEN no .env antes de rodar o bot.")
    bot.run(TOKEN)