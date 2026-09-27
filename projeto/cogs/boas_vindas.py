from __future__ import annotations

import os
import discord
from discord.ext import commands
from utils.views import enviar_embed

DONA_LUMINE_ID = int(os.getenv("DONA_LUMINE_ID", "0"))
DONA_AETHER_ID = int(os.getenv("DONA_AETHER_ID", "0"))
CANAL_BOAS_VINDAS_ID = int(os.getenv("CANAL_BOAS_VINDAS_ID", "0"))

BANNER_BV = "banners/boas_vindas.jpeg"


def montar_mensagem_bv() -> str:
    mencao_lumine = f"<@{DONA_LUMINE_ID}>"
    mencao_aether = f"<@{DONA_AETHER_ID}>"
    return f"""Paimon: Ei! Você finalmente chegou! :star:
Lumine e Aether estavam esperando por você!

Seja muito bem-vindo(a) à Traveler Store, um cantinho criado para todos aqueles que, assim como nós, estão sempre em busca de uma nova aventura. :crescent_moon::sparkles:

Aqui, você poderá conferir nossos serviços, realizar suas compras e encontrar tudo o que precisa para continuar sua jornada por Teyvat.

❝ Toda jornada começa com um primeiro passo.
Talvez o seu comece aqui. ❞

╭・✦・𝐀𝐧𝐭𝐞𝐬 𝐝𝐞 𝐜𝐨𝐦𝐞𝐜̧𝐚𝐫 𝐬𝐮𝐚 𝐣𝐨𝐫𝐧𝐚𝐝𝐚…
│
│ :scroll: Leia nossas [regras](https://discord.com/channels/1547070219045048371/1547091459419668480) e [termos de compra](https://discord.com/channels/1547070219045048371/1547090525398499328)
│ :shopping_bags: Confira [nossos serviços e produtos](https://discord.com/channels/1547070219045048371/1547246666107592734)
│ :ticket: Abra um [ticket](https://discord.com/channels/1547070219045048371/1547249019871297597) caso precise de ajuda
│ :love_letter: Deixe seu [feedback](https://discord.com/channels/1547070219045048371/1547245110167601276) após sua experiência
│
╰・✦・Boa viagem, Viajante!

Lumine ♡ Aether ♡ Paimon
estarão sempre por perto para acompanhar sua jornada. ✧

⋆｡°✩ Atenciosamente {mencao_lumine} ♡ {mencao_aether}. ✩°｡⋆"""


class BoasVindas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        canal = self.bot.get_channel(CANAL_BOAS_VINDAS_ID)
        if canal is None:
            print(f"[BV] Canal de boas-vindas não encontrado: {CANAL_BOAS_VINDAS_ID}")
            return

        # Verifica se o banner existe
        if os.path.exists(BANNER_BV):
            banner_path = BANNER_BV
        else:
            banner_path = None
            print(f"[BV] Banner não encontrado em '{BANNER_BV}', enviando sem imagem.")

        await enviar_embed(
            canal,
            "✦ 𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆 ✦",
            montar_mensagem_bv(),
            discord.Color.blurple(),
            banner_path=banner_path,
            content=member.mention,
        )

    # ---------- COMANDO DE TESTE ----------
    @commands.command(name="testebv")
    @commands.has_permissions(manage_guild=True)
    async def testebv(self, ctx: commands.Context):
        """Testa a mensagem de boas-vindas no canal atual."""
        if os.path.exists(BANNER_BV):
            banner_path = BANNER_BV
        else:
            banner_path = None
            await ctx.reply(
                f"⚠️ Banner não encontrado em `{BANNER_BV}`. "
                "Enviando sem imagem pra você testar o texto."
            )

        await enviar_embed(
            ctx,
            "✦ 𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆 ✦",
            montar_mensagem_bv(),
            discord.Color.blurple(),
            banner_path=banner_path,
            content=ctx.author.mention,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(BoasVindas(bot))