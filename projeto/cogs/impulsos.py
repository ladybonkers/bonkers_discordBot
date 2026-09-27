from __future__ import annotations

import discord
from discord.ext import commands
from utils.views import enviar_embed


def montar_mensagem_impulsos() -> str:
    return """Quer apoiar nossa jornada e ainda receber benefícios exclusivos?
Ao impulsionar a Traveler Store, desbloqueie vantagens especiais preparadas especialmente para nossos boosters. 🌟

🌙 𝐁𝐎𝐎𝐒𝐓 𝐋𝐕. 𝟏

✦ 5% de desconto em serviços da loja
✦ Cargo exclusivo de Booster
✦ Prioridade no atendimento dos seus tickets
✦ Acesso a sorteios e eventos exclusivos para boosters
✦ Nome personalizado entre os boosters do servidor

✧ 𝐁𝐎𝐎𝐒𝐓 𝐋𝐕. 𝟐

✦ 10% de desconto em serviços da loja
✦ Todas as vantagens do Boost Lv. 1
✦ Prioridade máxima no atendimento
✦ Participação com chance extra em sorteios exclusivos
✦ Acesso a um canal exclusivo para boosters
✦ Uma vantagem mensal especial em um serviço da Traveler Store

🗺️ 𝐏𝐎𝐑 𝐐𝐔𝐄 𝐁𝐎𝐎𝐒𝐓𝐀𝐑?

Cada boost ajuda a Traveler Store a melhorar, crescer e trazer novos serviços, eventos e benefícios para toda a comunidade.
Seu apoio faz parte da nossa jornada. ♡

⚠️ 𝐀𝐕𝐈𝐒𝐎 𝐀𝐎𝐒 𝐕𝐈𝐀𝐉𝐀𝐍𝐓𝐄𝐒

As recompensas são destinadas aos membros que mantêm seu boost ativo no servidor. Caso o boost seja retirado, os benefícios correspondentes serão suspensos (banimento da loja ) 

Em caso de dúvidas sobre o sistema de boosters, fale com nossa equipe no canal [・💬・dúvidas](https://discord.com/channels/1547070219045048371/1547251513989013644)."""


class Impulsos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="impulsos")
    @commands.has_permissions(manage_guild=True)
    async def impulsos(self, ctx: commands.Context):
        await enviar_embed(
            ctx,
            "✦ 𝐒𝐄𝐉𝐀 𝐁𝐎𝐎𝐒𝐓𝐄𝐑 𝐃𝐀 𝐓𝐑𝐀𝐕𝐄𝐋𝐄𝐑 𝐒𝐓𝐎𝐑𝐄 ✦",
            montar_mensagem_impulsos(),
            discord.Color.purple(),
            rodape="Atenciosamente — Traveler Store 🌙",
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Impulsos(bot))