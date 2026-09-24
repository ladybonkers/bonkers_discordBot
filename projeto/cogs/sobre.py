from __future__ import annotations

import discord
from discord.ext import commands
from Bonkers_DiscordBot.projeto.utils.views import enviar_embed


def montar_mensagem_sobre() -> str:
    return """Somos uma loja focada em serviços de Genshin Impact, criada com o objetivo de oferecer um atendimento seguro, organizado e, acima de tudo, de confiança para nossos clientes. Aqui, cada pessoa da equipe possui uma função importante para que tudo funcione da melhor maneira possível. Conheça nossos cargos:

╭・ ✦ ***DONOS***
São os responsáveis pela loja como um todo e pelas principais decisões da Traveler Store. Cuidam para que a loja continue crescendo e funcionando da melhor forma.

╭・ ✦ ***ADMINISTRADORES***
Cuidam da organização e administração geral do servidor, incluindo sua estrutura, canais, cargos e funcionamento interno.

╭・ ✦ ***MODERADORES***
São responsáveis por manter a ordem no servidor, auxiliar os membros e moderar os chats quando necessário. Nosso objetivo é sempre manter um ambiente tranquilo, respeitoso e agradável para todos.

╭・ ✦ ***FARMERS***
Os Farmers são uma das partes mais importantes da nossa loja. Eles são os responsáveis por colocar os serviços em prática e fazer os pedidos dos nossos clientes acontecerem. São praticamente as pernas da Traveler Store: enquanto a equipe organiza e administra a loja, são eles que entram em ação para realizar os serviços. Seja um farm de giros, sessão de personagem, build, missões de Arconte, missões lendárias ou alguma missão específica, nossos Farmers são aqueles que irão realizar o serviço solicitado pelo cliente, sempre buscando cumprir o pedido da melhor maneira possível.

╭・ ✦ ***EQUIPE***
Todos que fazem parte da equipe possuem um papel importante dentro da Traveler Store. Trabalhamos juntos para oferecer um serviço cada vez melhor e uma experiência tranquila para nossos clientes."""


class Sobre(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sobre")
    @commands.has_permissions(manage_guild=True)
    async def sobre(self, ctx: commands.Context):
        await enviar_embed(
            ctx,
            "୨୧ • Apresentação da Equipe",
            montar_mensagem_sobre(),
            discord.Color.blurple(),
            rodape="Atenciosamente — Traveler Store 🌙",
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Sobre(bot))