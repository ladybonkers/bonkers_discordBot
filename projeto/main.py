from __future__ import annotations

import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Garante que "utils" e "cogs" sejam encontrados mesmo se rodar de outra pasta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    "cogs.admin",
]


@bot.event
async def setup_hook():
    # Carrega todos os cogs
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"[OK] Cog carregado: {cog}")
        except Exception as e:
            print(f"[ERRO] Falha ao carregar {cog}: {e}")

    # ---- Views persistentes (sobrevivem a restart do bot) ----
    from cogs.tickets import PainelTicketView, TicketAbertoView

    bot.add_view(PainelTicketView())
    bot.add_view(TicketAbertoView())

    print("[OK] Views persistentes registradas.")


@bot.event
async def on_ready():
    print(f"Bot online como {bot.user} (ID: {bot.user.id})")
    print(f"Servidores: {len(bot.guilds)}")

    canal_logs_id = int(os.getenv("CANAL_LOGS_ID", "0"))
    dona_aether = os.getenv("DONA_AETHER_ID", "0")
    canal_logs = bot.get_channel(canal_logs_id)
    if canal_logs:
        try:
            await canal_logs.send(
                f"🟢 **{bot.user.name}** está online agora! Vai tomando <@{dona_aether}>"
            )
        except discord.HTTPException as e:
            print(f"[LOG] Erro ao mandar mensagem de log: {e}")


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Defina DISCORD_TOKEN no .env antes de rodar o bot.")
    bot.run(TOKEN)