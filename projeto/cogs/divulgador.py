from __future__ import annotations

import discord
from discord.ext import commands
from Bonkers_DiscordBot.projeto.utils.views import enviar_embed


def montar_mensagem_divulgador() -> str:
    return "Em breve você verá aqui as informações sobre nosso programa de divulgação!"


class Divulgador(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="divulgador")
    @commands.has_permissions(manage_guild=True)
    async def divulgador(self, ctx: commands.Context):
        await enviar_embed(
            ctx,
            "📣 Programa Divulgador — Traveler Store",
            montar_mensagem_divulgador(),
            discord.Color.orange(),
            rodape="Divulgue a Traveler Store e ganhe recompensas!",
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Divulgador(bot))