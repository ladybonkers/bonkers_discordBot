from __future__ import annotations

import discord
from discord.ext import commands
from Bonkers_DiscordBot.projeto.utils.views import enviar_embed


def montar_mensagem_fb() -> str:
    return """♡ 𝑺𝒖𝒂 𝒐𝒑𝒊𝒏𝒊𝒂̃𝒐 𝒆́ 𝒎𝒖𝒊𝒕𝒐 𝒊𝒎𝒑𝒐𝒓𝒕𝒂𝒏𝒕𝒆 𝒑𝒂𝒓𝒂 𝒏𝒐́𝒔! ♡

Este é o espaço reservado para você compartilhar sua experiência com a Traveler Store. Depois de realizar um serviço conosco, conte para a gente como foi sua experiência e ajude nossa loja a continuar crescendo! ✦"""


class Feedback(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="feedback")
    @commands.has_permissions(manage_guild=True)
    async def feedback(self, ctx: commands.Context):
        await enviar_embed(
            ctx,
            "✦ 𝑭𝑬𝑬𝑫𝑩𝑨𝑪𝑲𝑺 ✦",
            montar_mensagem_fb(),
            discord.Color.blurple(),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Feedback(bot))