from __future__ import annotations

import discord
from discord.ext import commands
from Bonkers_DiscordBot.projeto.utils.views import enviar_embed


def montar_mensagem_regras() -> str:
    return """Bem-vindo(a) à nossa loja, Viajante. Antes de partir em jornada conosco, leia com atenção as diretrizes abaixo — elas existem para manter Teyvat um lugar tranquilo para todos.

Ao permanecer no servidor, você concorda com estas regras. A administração poderá aplicar punições conforme a gravidade.

**✦ ─── 01 · Respeito acima de tudo ─── ✦**

Trate todos com educação — membros, clientes, farmers e equipe. Ofensas, assédio, ameaças, preconceito ou discurso de ódio não têm espaço aqui. Brincadeiras são bem-vindas, mas param quando alguém pedir. Conflitos pessoais devem ser resolvidos na DM, não no chat.

**✦ ─── 02 · Canais organizados ─── ✦**

Cada canal tem uma função — use o canal certo para cada coisa. Compras, dúvidas e atendimentos só pelo sistema oficial de tickets. Mensagens fora de contexto podem ser removidas sem aviso.

**✦ ─── 03 · Sem spam ou flood ─── ✦**

Nada de mensagens repetidas, excesso de emojis, CAPS LOCK gritante ou marcações desnecessárias. Divulgação de links, outras lojas ou serviços só com autorização da administração.

**✦ ─── 04 · Compras e atendimento ─── ✦**

Antes de comprar, leia preços, prazos e termos do serviço. Os pedidos são atendidos por ordem de chegada ou disponibilidade da equipe. Não marque staff repetidamente pra "acelerar" — isso atrapalha em vez de ajudar. Confirme sempre se está falando com alguém da equipe oficial antes de pagar.

**✦ ─── 05 · Conta e segurança ─── ✦**

Nunca compartilhe senhas ou códigos com quem não faz parte da equipe oficial. Forneça apenas o que for pedido pelos procedimentos oficiais. A Traveler Store não se responsabiliza por negociações feitas fora dos nossos canais. Suspeitou de alguém se passando por staff? Reporte à administração imediatamente.

**✦ ─── 06 · Conduta e conteúdo ─── ✦**

Proibido conteúdo adulto, violento, ilegal ou que viole as diretrizes do Discord — isso vale para mensagens, imagens, links, nomes, avatares e status. Fraudes, golpes ou comprovantes falsos resultam em banimento imediato. Negociações paralelas por DM também são proibidas.

**✦ ─── 07 · Punições ─── ✦**

As medidas seguem a gravidade, frequência e contexto de cada situação. Podem incluir: advertência, mute, restrição de canais, expulsão ou banimento. Casos graves podem ser punidos sem aviso prévio.

**✦ ─── ✦ ─── ✦**

Ao permanecer no servidor, você confirma que leu e concorda com estas regras. Boa jornada por Teyvat, Viajante. 🌙"""


class Regras(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="regras")
    @commands.has_permissions(manage_guild=True)
    async def regras(self, ctx: commands.Context):
        await enviar_embed(
            ctx,
            "✦ 𝑅𝐸𝐺𝑅𝐴𝑆 · 𝑇𝑅𝐴𝑉𝐸𝐿𝐸𝑅 𝑆𝑇𝑂𝑅𝐸 ✦",
            montar_mensagem_regras(),
            discord.Color.gold(),
            rodape="A Traveler Store poderá atualizar estas regras sempre que necessário.",
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Regras(bot))