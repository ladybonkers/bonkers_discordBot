from __future__ import annotations

import discord
from discord.ext import commands
from utils.views import enviar_embed


def montar_mensagem_compra() -> str:
    return f""" ── 𝐒𝐮𝐚 𝐣𝐨𝐫𝐧𝐚𝐝𝐚 𝐜𝐨𝐦𝐞𝐜̧𝐚 𝐚𝐪𝐮𝐢! ✦

・🌟 𝐏𝐫𝐞𝐜𝐢𝐬𝐚 𝐝𝐞 𝐚𝐣𝐮𝐝𝐚?
Qualquer dúvida antes de realizar seu pedido? Mande sua pergunta no canal 
[・💬・dúvidas](https://discord.com/channels/1547070219045048371/1547251513989013644)! Nossa equipe ou membros da comunidade estarão prontos para ajudar e responder o mais rápido possível.

・💰 𝐂𝐨𝐧𝐬𝐮𝐥𝐭𝐞 𝐧𝐨𝐬𝐬𝐨𝐬 𝐩𝐫𝐞𝐜̧𝐨𝐬
Antes de comprar, confira nossa tabela de preços para conhecer todos os serviços disponíveis e seus respectivos valores: ➜ [・💸・preços](https://discord.com/channels/1547070219045048371/1548378994385227866)

・💌 𝐀𝐢𝐧𝐝𝐚 𝐞𝐬𝐭𝐚́ 𝐢𝐧𝐬𝐞𝐠𝐮𝐫𝐨(𝐚)?
Sem problemas! Você pode conferir nosso canal de feedbacks e conhecer as experiências de clientes que já passaram pela Traveler Store. ✨ ➜ [・📩・feedbacks](https://discord.com/channels/1547070219045048371/1547245110167601276)

・🎫 𝐏𝐫𝐨𝐧𝐭𝐨 𝐩𝐚𝐫𝐚 𝐬𝐮𝐚 𝐣𝐨𝐫𝐧𝐚𝐝𝐚?
Crie seu ticket de atendimento pelo canal abaixo e nossa equipe irá atendê-lo para realizar seu pedido! ➜ [・🛒・compre-aqui](https://discord.com/channels/1547070219045048371/1547249019871297597)"""


class Compras(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="compras")
    @commands.has_permissions(manage_guild=True)
    async def compras(self, ctx: commands.Context):
        await enviar_embed(
            ctx,
            "୨୧ • Como Comprar na Traveler Store",
            montar_mensagem_compra(),
            discord.Color.gold(),
            rodape="Traveler Store —  Seu pedido, nossa missão.",
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Compras(bot))