from __future__ import annotations

import discord
from discord.ext import commands


# ==================================================================
# DADOS DOS PREÇOS
# ==================================================================
CATEGORIAS: dict[str, dict] = {
    "gemas": {
        "label": "Gemas",
        "emoji": "💎",
        "texto": (
            "800 Gemas — **R$9,00** (5 giros)\n"
            "1.600 Gemas — **R$18,00** (10 giros)\n"
            "3.200 Gemas — **R$28,00** (20 giros)\n"
            "4.800 Gemas — **R$38,00** (30 giros)\n"
            "6.400 Gemas — **R$48,00** (40 giros)\n"
            "8.000 Gemas — **R$58,00** (50 giros)\n"
            "9.600 Gemas — **R$68,00** (60 giros)\n"
            "11.200 Gemas — **R$78,00** (70 giros)\n"
            "12.800 Gemas — **R$88,00** (80 giros)\n"
            "14.400 Gemas — **R$98,00** (90 giros)\n"
            "16.000 Gemas — **R$108,00** (100 giros)"
        ),
    },
    "oculus": {
        "label": "Oculus",
        "emoji": "🔮",
        "texto": (
            "Anemoculus — **R$30,00**\n"
            "Geoculus — **R$45,00**\n"
            "Electroculus — **R$40,00**\n"
            "Dendroculus — **R$65,00**\n"
            "Hydroculus — **R$60,00**\n"
            "Pyroculus — **R$70,00**\n"
            "Carmesim — **R$20,00** (até o Lv. 8)\n"
            "Carmesim Completo — **R$25,00**\n"
            "Lumen — **R$40,00**\n"
            "Carpas — **R$38,00**\n"
            "Plumas — **R$40,00**\n"
            "Lunoculos — **R$60,00**\n\n"
            "-# Existe desconto dependendo do nível da estátua."
        ),
    },
    "exploracao": {
        "label": "Exploração 100%",
        "emoji": "🗺️",
        "texto": (
            "Mondstadt — **R$40,00**\n"
            "Espinha do Dragão — **R$35,00**\n"
            "Liyue — **R$80,00**\n"
            "Despenhadeiro + Minas Subterrâneas — **R$60,00**\n"
            "Inazuma — **R$70,00**\n"
            "Enkanomiya — **R$60,00**\n"
            "Sumeru Floresta — **R$85,00**\n"
            "Sumeru Deserto — **R$100,00**\n"
            "Fontaine — **R$95,00**\n"
            "Mar Antigo — **R$50,00**\n"
            "Vale Chenyu — **R$50,00**\n"
            "Natlan — **R$95,00**\n"
            "Atocpan — **R$50,00**\n"
            "Resort da Brisa — **R$60,00**\n"
            "Nodkrai — **R$100,00**\n"
            "A Lua — **R$69,00**\n"
            "Montanha Sagrada — **R$45,00**\n"
            "Pico do Repouso — **R$30,00**\n"
            "Templo do Espaço — **R$50,00**\n"
            "Snezhnaya — **R$98,00**\n\n"
            "-# Existe desconto dependendo da porcentagem de exploração.\n"
            "-# A exploração 100% não inclui missões da área."
        ),
    },
    "progressao": {
        "label": "Progressão de Personagens",
        "emoji": "⭐",
        "texto": (
            "Por ascensão — **R$6,00**\n"
            "Lv. 1 → 90 completo — **R$35,00**\n"
            "Arma Lv. 1 → 90 — **R$15,00**\n"
            "3 talentos Lv. 10 — **R$36,00** (R$12 cada)\n"
            "Item de Boss — **R$0,40** cada\n"
            "64 Itens de Boss — **R$25,00**"
        ),
    },
    "farm_armas": {
        "label": "Farm de Armas",
        "emoji": "⚔️",
        "texto": (
            "Fisgada ou Cano — **R$22,00**\n"
            "R1 → R5 — **R$36,00**\n"
            "Refino único — **R$6,00**"
        ),
    },
    "builds": {
        "label": "Builds",
        "emoji": "🛠️",
        "texto": (
            "Básica — **R$10,00**\n"
            "Média — **R$15,00**\n"
            "Excelente — **R$25,00**\n"
            "Ajustes na build, sem farm — **R$6,00**\n\n"
            "-# Caso não possua resinas na conta, será aplicada uma taxa de 16%."
        ),
    },
    "manutencao": {
        "label": "Manutenção de Conta",
        "emoji": "🔧",
        "texto": (
            "Diárias — **R$1,20**\n"
            "Pacote mensal de Diárias — **R$30,00**\n"
            "Resinas — **R$1,30**\n"
            "Pacote mensal de Resinas — **R$30,00**\n"
            "Diárias + Resinas — **R$1,50**\n"
            "Pacote mensal Diárias + Resinas — **R$35,00**\n"
            "Reputação semanal — **R$5,00**"
        ),
    },
    "missoes": {
        "label": "Missões",
        "emoji": "📜",
        "texto": (
            "Mundo Simples — **R$7,00**\n"
            "Mundo Complexa — **R$14,00**\n"
            "Lendária — **R$10,00**\n"
            "Encontro — **R$10,00**\n"
            "Arconte — **R$15,00** (por ato)\n"
            "Cadeia de Missões dos Aranaras Completa — **R$100,00**\n"
            "Aranaras — **R$80,00**\n"
            "Missão da Ilha Tsurumi — **R$30,00**"
        ),
    },
    "eventos": {
        "label": "Eventos",
        "emoji": "🎉",
        "texto": (
            "Comum — **R$15,00**\n"
            "Complexo — **R$21,00**\n"
            "Evento Fontinalia Completo — **R$40,00**"
        ),
    },
    "tcg": {
        "label": "TCG",
        "emoji": "🎴",
        "texto": (
            "Lv. 1 → 10 — **R$35,00**\n"
            "Lv. 2 → 10 — **R$32,00**\n"
            "Lv. 3 → 10 — **R$28,00**\n"
            "Lv. 4 → 10 — **R$24,00**\n"
            "Lv. 5 → 10 — **R$20,00**\n"
            "Lv. 6 → 10 — **R$18,00**\n"
            "Lv. 7 → 10 — **R$15,00**\n"
            "Lv. 8 → 10 — **R$12,00**\n"
            "Lv. 9 → 10 — **R$8,00**"
        ),
    },
    "bule": {
        "label": "Bule de Relachá",
        "emoji": "🫖",
        "texto": (
            "Por nível do Bule — **R$6,00**\n"
            "Lv. 1 → 10 — **R$55,00**"
        ),
    },
    "abismo": {
        "label": "End Game — Abismo",
        "emoji": "🏆",
        "texto": (
            "Piso único — **R$8,00**\n"
            "Andares 11 e 12 — **R$16,00**\n"
            "Andares 9, 10, 11 e 12 — **R$30,00**\n"
            "Andares 1 → 12 — **R$50,00**\n\n"
            "-# No modo manual, a conta será avaliada para verificar se é possível "
            "realizar o End Game normalmente."
        ),
    },
    "teatro": {
        "label": "End Game — Teatro",
        "emoji": "🎭",
        "texto": (
            "Fácil — **R$12,00**\n"
            "Médio — **R$18,00**\n"
            "Difícil — **R$27,00**\n"
            "Visionário — **R$34,00**\n"
            "Lunar — **R$41,00**\n"
            "Rastro — **R$8,00**"
        ),
    },
    "confronto": {
        "label": "Confronto Abissal",
        "emoji": "🌑",
        "texto": (
            "Completo com a Skin — **R$45,00**\n"
            "Até as Penas — **R$30,00**\n"
            "Somente as Gemas — **R$18,00**"
        ),
    },
    "extras": {
        "label": "Extras",
        "emoji": "➕",
        "texto": (
            "Flores de personagem — **R$0,20** cada\n"
            "Lendas Locais — **R$3,00** cada requisito\n"
            "Uma Lenda Local completa — **R$8,50**\n"
            "Borboletas — **R$0,30** cada\n"
            "50 Borboletas — **R$15,00**\n"
            "Minérios — **R$0,30** cada"
        ),
    },
    "packs": {
        "label": "Packs Especiais",
        "emoji": "🎁",
        "texto": (
            "**𝐂𝐨𝐦𝐛𝐨 𝐅𝐥𝐢𝐧𝐬 𝐎𝐔 𝐈𝐧𝐞𝐟𝐟𝐚 — 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐌𝐚́𝐱𝐢𝐦𝐨**\n"
            "・ Ascensão Lv. 1 → 90\n"
            "・ 2 talentos → Lv. 10\n"
            "・ Build Excelente\n\n"
            "Valor: **R$70,00**"
        ),
    },
}


COR = discord.Color.gold()
TITULO = "𝐓𝐑𝐀𝐕𝐄𝐋𝐄𝐑 𝐒𝐓𝐎𝐑𝐄 ✦ 𝐆𝐞𝐧𝐬𝐡𝐢𝐧 𝐈𝐦𝐩𝐚𝐜𝐭 — 𝐓𝐚𝐛𝐞𝐥𝐚 𝐝𝐞 𝐏𝐫𝐞𝐜̧𝐨𝐬・୨୧"
RODAPE = "୨୧・𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆 — Onde sua jornada começa. ᰔ"


def texto_menu_principal() -> str:
    linhas = [f"˚₊‧ `{d['emoji']}` {d['label']}" for d in CATEGORIAS.values()]
    return (
        " ࣪˖ ִֶָ Aqui você encontra nossa tabelinha de preços para os nossos serviços\n "
        "Cada pedido é tratado como uma nova jornada — feita com dedicação, "
        "segurança e carinho.\n\n"
        "˚₊‧𝐄𝐬𝐜𝐨𝐥𝐡𝐚 𝐮𝐦𝐚 𝐜𝐚𝐭𝐞𝐠𝐨𝐫𝐢𝐚 𝐚𝐛𝐚𝐢𝐱𝐨 𝐩𝐚𝐫𝐚 𝐜𝐨𝐧𝐟𝐞𝐫𝐢𝐫 𝐨𝐬 𝐯𝐚𝐥𝐨𝐫𝐞𝐬!\n\n"
        + "\n".join(linhas)
        + "\n\n"
        "˚₊‧ Gostou? Então entre em contato com a gente [﹒🛒﹕compre-aqui](https://discord.com/channels/1547070219045048371/1547249019871297597)!\n\n"
        "-# Os preços podem ser ajustados conforme a necessidade do serviço.\n"
        "-# Consulte sempre o ticket para confirmar o valor final."
    )


def montar_embed_categoria(chave: str) -> discord.Embed:
    """Monta o embed de uma categoria específica."""
    dados = CATEGORIAS[chave]
    embed = discord.Embed(
        title=f"˚₊‧・{dados['emoji']} {dados['label']} — Traveler Store",
        description=dados["texto"],
        color=COR,
    )
    embed.set_footer(text=RODAPE)
    return embed


# ==================================================================
# VIEW PRINCIPAL — postada no canal, visível a todos
# ==================================================================
class MenuPrecosView(discord.ui.View):
    """View pública com UM select só. Ao escolher, responde EPHEMERAL."""

    def __init__(self):
        super().__init__(timeout=None)

        select = discord.ui.Select(
            placeholder="Escolha uma categoria...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=dados["label"],
                    value=chave,
                    emoji=dados["emoji"],
                )
                for chave, dados in CATEGORIAS.items()
            ][:25],
            custom_id="precos_menu_principal",
        )
        select.callback = self.selecionar
        self.add_item(select)

    async def selecionar(self, interaction: discord.Interaction):
        chave = interaction.data["values"][0]

        await interaction.response.send_message(
            embed=montar_embed_categoria(chave),
            view=VerOutraCategoriaView(chave_atual=chave),
            ephemeral=True,
        )


# ==================================================================
# VIEW SECUNDÁRIA — aparece no ephemeral (só o autor vê)
# ==================================================================
class VerOutraCategoriaView(discord.ui.View):
    """Permite trocar de categoria sem sair do ephemeral."""

    def __init__(self, chave_atual: str):
        super().__init__(timeout=180)
        self.chave_atual = chave_atual

        select = discord.ui.Select(
            placeholder="Ver outra categoria...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=dados["label"],
                    value=chave,
                    emoji=dados["emoji"],
                    default=(chave == chave_atual),
                )
                for chave, dados in CATEGORIAS.items()
            ][:25],
            custom_id="precos_ephemeral_trocar",
        )
        select.callback = self.trocar
        self.add_item(select)

    async def trocar(self, interaction: discord.Interaction):
        chave = interaction.data["values"][0]
        await interaction.response.edit_message(
            embed=montar_embed_categoria(chave),
            view=VerOutraCategoriaView(chave_atual=chave),
        )


# ==================================================================
# COG
# ==================================================================
class Precos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="precos")
    @commands.has_permissions(manage_guild=True)
    async def precos(self, ctx: commands.Context):
        embed = discord.Embed(
            title=TITULO,
            description=texto_menu_principal(),
            color=COR,
        )
        embed.set_footer(text=RODAPE)
        await ctx.send(embed=embed, view=MenuPrecosView())


async def setup(bot: commands.Bot):
    await bot.add_cog(Precos(bot))