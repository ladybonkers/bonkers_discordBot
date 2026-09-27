from __future__ import annotations

import discord
from discord.ext import commands


# ==================================================================
# TABELA MANUAL
# ==================================================================
SERVICOS_MANUAL: dict[str, dict] = {
    "gemas": {
        "label": "Gemas", "emoji": "💎",
        "itens": [
            ("800 Gemas (5 giros)", "R$8,00"),
            ("1.600 Gemas (10 giros)", "R$14,00"),
            ("3.200 Gemas (20 giros)", "R$28,00"),
            ("4.800 Gemas (30 giros)", "R$38,00"),
            ("6.400 Gemas (40 giros)", "R$48,00"),
            ("8.000 Gemas (50 giros)", "R$58,00"),
            ("9.600 Gemas (60 giros)", "R$68,00"),
            ("11.200 Gemas (70 giros)", "R$78,00"),
            ("12.800 Gemas (80 giros)", "R$88,00"),
            ("14.400 Gemas (90 giros)", "R$98,00"),
            ("16.000 Gemas (100 giros)", "R$108,00"),
        ],
    },
    "oculus": {
        "label": "Oculi", "emoji": "🔮",
        "itens": [
            ("Anemoculus", "R$30,00"),
            ("Geoculus", "R$45,00"),
            ("Electroculus", "R$40,00"),
            ("Dendroculus", "R$65,00"),
            ("Hydroculus", "R$60,00"),
            ("Pyroculus", "R$70,00"),
            ("Carmesim (até Lv. 8)", "R$20,00"),
            ("Carmesim Completo", "R$25,00"),
            ("Lumen", "R$40,00"),
            ("Carpas", "R$38,00"),
            ("Plumas", "R$40,00"),
            ("Lunoculos", "R$60,00"),
        ],
        "nota": "Existe desconto dependendo do nível da estátua.",
    },
    "exploracao": {
        "label": "Exploração", "emoji": "🗺️",
        "itens": [
            ("Mondstadt", "R$40,00"),
            ("Espinha do Dragão", "R$35,00"),
            ("Liyue", "R$80,00"),
            ("Despenhadeiro + Minas Subterrâneas", "R$60,00"),
            ("Inazuma", "R$70,00"),
            ("Enkanomiya", "R$60,00"),
            ("Sumeru Floresta", "R$85,00"),
            ("Sumeru Deserto", "R$100,00"),
            ("Fontaine", "R$95,00"),
            ("Mar Antigo", "R$50,00"),
            ("Vale Chenyu", "R$50,00"),
            ("Natlan", "R$95,00"),
            ("Atocpan", "R$50,00"),
            ("Resort da Brisa", "R$60,00"),
            ("Nodkrai", "R$100,00"),
            ("A Lua", "R$69,00"),
            ("Montanha Sagrada", "R$45,00"),
            ("Pico do Repouso", "R$30,00"),
            ("Templo do Espaço", "R$50,00"),
            ("Snezhnaya", "R$98,00"),
        ],
        "nota": "Existe desconto dependendo da porcentagem de exploração.\nA exploração 100% não inclui missões da área.",
    },
    "progressao": {
        "label": "Progressão", "emoji": "⭐",
        "itens": [
            ("Por ascensão", "R$6,00"),
            ("Lv. 1 → 90 completo", "R$35,00"),
            ("Arma Lv. 1 → 90", "R$15,00"),
            ("3 talentos Lv. 10", "R$36,00"),
            ("Item de Boss (cada)", "R$0,40"),
            ("64 Itens de Boss", "R$25,00"),
        ],
    },
    "farm_armas": {
        "label": "Farm de Armas", "emoji": "⚔️",
        "itens": [
            ("Fisgada ou Cano", "R$22,00"),
            ("R1 → R5", "R$36,00"),
            ("Refino único", "R$6,00"),
        ],
    },
    "builds": {
        "label": "Builds", "emoji": "🛠️",
        "itens": [
            ("Básica", "R$10,00"),
            ("Média", "R$15,00"),
            ("Excelente", "R$25,00"),
            ("Ajustes na build, sem farm", "R$6,00"),
        ],
        "nota": "Caso não possua resinas na conta, será aplicada uma taxa de 16%.",
    },
    "manutencao": {
        "label": "Manutenção", "emoji": "🔧",
        "itens": [
            ("Diárias (por dia)", "R$1,20"),
            ("Pacote mensal de Diárias", "R$30,00"),
            ("Resinas (por dia)", "R$1,30"),
            ("Pacote mensal de Resinas", "R$30,00"),
            ("Diárias + Resinas (por dia)", "R$1,50"),
            ("Pacote mensal Diárias + Resinas", "R$35,00"),
            ("Reputação semanal", "R$5,00"),
        ],
    },
    "missoes": {
        "label": "Missões", "emoji": "📜",
        "itens": [
            ("Mundo Simples", "R$7,00"),
            ("Mundo Complexa", "R$14,00"),
            ("Lendária", "R$10,00"),
            ("Encontro", "R$10,00"),
            ("Arconte (por ato)", "R$15,00"),
            ("Cadeia dos Aranaras Completa", "R$100,00"),
            ("Aranaras", "R$80,00"),
            ("Ilha Tsurumi", "R$30,00"),
        ],
    },
    "eventos": {
        "label": "Eventos", "emoji": "🎉",
        "itens": [
            ("Comum", "R$15,00"),
            ("Complexo", "R$21,00"),
            ("Fontinalia Completo", "R$40,00"),
        ],
    },
    "tcg": {
        "label": "TCG", "emoji": "🎴",
        "itens": [
            ("Lv. 1 → 10", "R$35,00"),
            ("Lv. 2 → 10", "R$32,00"),
            ("Lv. 3 → 10", "R$28,00"),
            ("Lv. 4 → 10", "R$24,00"),
            ("Lv. 5 → 10", "R$20,00"),
            ("Lv. 6 → 10", "R$18,00"),
            ("Lv. 7 → 10", "R$15,00"),
            ("Lv. 8 → 10", "R$12,00"),
            ("Lv. 9 → 10", "R$8,00"),
        ],
    },
    "bule": {
        "label": "Bule de Relachá", "emoji": "🫖",
        "itens": [
            ("Por nível do Bule", "R$6,00"),
            ("Lv. 1 → 10", "R$55,00"),
        ],
    },
    "abismo": {
        "label": "End Game — Abismo", "emoji": "🏆",
        "itens": [
            ("Piso único", "R$8,00"),
            ("Andares 11 e 12", "R$16,00"),
            ("Andares 9, 10, 11 e 12", "R$30,00"),
            ("Andares 1 → 12", "R$50,00"),
        ],
        "nota": "No modo manual, a conta será avaliada para verificar se é possível realizar o End Game normalmente.",
    },
    "teatro": {
        "label": "End Game — Teatro", "emoji": "🎭",
        "itens": [
            ("Fácil", "R$12,00"),
            ("Médio", "R$18,00"),
            ("Difícil", "R$27,00"),
            ("Visionário", "R$34,00"),
            ("Lunar", "R$41,00"),
            ("Rastro", "R$8,00"),
        ],
    },
    "confronto": {
        "label": "Confronto Abissal", "emoji": "🌑",
        "itens": [
            ("Completo com a Skin", "R$45,00"),
            ("Até as Penas", "R$30,00"),
            ("Somente as Gemas", "R$18,00"),
        ],
    },
    "extras": {
        "label": "Extras", "emoji": "➕",
        "itens": [
            ("Flores de personagem (cada)", "R$0,20"),
            ("Lendas Locais (cada requisito)", "R$3,00"),
            ("Uma Lenda Local completa", "R$8,50"),
            ("Borboletas (cada)", "R$0,30"),
            ("50 Borboletas", "R$15,00"),
            ("Minérios (cada)", "R$0,30"),
        ],
    },
    "packs": {
        "label": "Packs Especiais", "emoji": "🎁",
        "itens": [
            ("Combo Flins/Ineffa — Upgrade Máximo", "R$70,00"),
        ],
        "nota": "Consulte nossa equipe para contratar ou tirar dúvidas.",
    },
}


# ==================================================================
# TABELA SCRIPT
# ==================================================================
SERVICOS_SCRIPT: dict[str, dict] = {
    "gemas": {
    "label": "Gemas", "emoji": "💎",
    "subgrupos": [
        {
            "titulo": "Exploração abaixo de 50%",
            "itens": [
                ("800 Gemas (5 giros)", "R$8,00"),
                ("1.600 Gemas (10 giros)", "R$13,00"),
                ("3.200 Gemas (20 giros)", "R$23,00"),
                ("4.800 Gemas (30 giros)", "R$33,00"),
                ("6.400 Gemas (40 giros)", "R$43,00"),
                ("8.000 Gemas (50 giros)", "R$53,00"),
                ("9.600 Gemas (60 giros)", "R$63,00"),
                ("11.200 Gemas (70 giros)", "R$73,00"),
                ("12.800 Gemas (80 giros)", "R$83,00"),
                ("14.400 Gemas (90 giros)", "R$93,00"),
                ("16.000 Gemas (100 giros)", "R$103,00"),
            ],
        },
        {
            "titulo": "Exploração acima de 50%",
            "itens": [
                ("800 Gemas (5 giros)", "R$8,00"),
                ("1.600 Gemas (10 giros)", "R$17,00"),
                ("3.200 Gemas (20 giros)", "R$27,00"),
                ("4.800 Gemas (30 giros)", "R$37,00"),
                ("6.400 Gemas (40 giros)", "R$47,00"),
                ("8.000 Gemas (50 giros)", "R$57,00"),
                ("9.600 Gemas (60 giros)", "R$67,00"),
                ("11.200 Gemas (70 giros)", "R$77,00"),
                ("12.800 Gemas (80 giros)", "R$87,00"),
                ("14.400 Gemas (90 giros)", "R$97,00"),
                ("16.000 Gemas (100 giros)", "R$109,00"),
            ],
        },
    ],
    "nota": "O valor varia conforme a porcentagem de exploração da sua conta.",
},
    "oculus": {
        "label": "Oculi", "emoji": "🔮",
        "itens": [
            ("Anemoculus", "R$12,00"),
            ("Geoculus", "R$19,00"),
            ("Electroculus", "R$27,00"),
            ("Dendroculus", "R$39,00"),
            ("Hydroculus", "R$39,00"),
            ("Pyroculus", "R$39,00"),
            ("Carmesim (até Lv. 8)", "R$11,00"),
            ("Carmesim Completo", "R$19,00"),
            ("Lumen", "R$24,00"),
            ("Carpas", "R$24,00"),
            ("Plumas", "R$31,00"),
            ("Lunoculos", "R$41,00"),
            ("Cryoculus", "R$39,00"),
        ],
        "nota": "Pode haver desconto conforme o nível da estátua.",
    },
    "exploracao": {
        "label": "Exploração", "emoji": "🗺️",
        "itens": [
            ("Mondstadt", "R$29,00"),
            ("Espinha do Dragão", "R$29,00"),
            ("Liyue", "R$39,00"),
            ("Despenhadeiro + Minas Subterrâneas", "R$59,00"),
            ("Inazuma", "R$69,00"),
            ("Enkanomiya", "R$59,00"),
            ("Sumeru Floresta", "R$84,00"),
            ("Sumeru Deserto", "R$99,00"),
            ("Fontaine", "R$94,00"),
            ("Mar Antigo", "R$49,00"),
            ("Vale Chenyu", "R$49,00"),
            ("Natlan", "R$94,00"),
            ("Atocpan", "R$49,00"),
            ("Resort da Brisa", "R$59,00"),
            ("Nodkrai", "R$89,00"),
            ("A Lua", "R$58,00"),
            ("Montanha Sagrada", "R$44,00"),
            ("Pico do Repouso", "R$22,00"),
            ("Templo do Espaço", "R$47,00"),
            ("Snezhnaya", "R$78,00"),
        ],
        "nota": "O valor pode variar de acordo com a porcentagem de exploração da região.\nExploração 100% não inclui as missões da área.",
    },
    "progressao": {
        "label": "Progressão", "emoji": "⭐",
        "itens": [
            ("Por ascensão", "R$4,00"),
            ("Lv. 1 → 90 completo", "R$24,00"),
            ("Arma Lv. 1 → 90", "R$14,00"),
            ("3 talentos Lv. 10", "R$35,00"),
            ("Item de Boss (cada)", "R$0,20"),
        ],
    },
    "farm_armas": {
        "label": "Farm de Armas", "emoji": "⚔️",
        "itens": [
            ("Fisgada ou Cano", "R$19,00"),
            ("R1 → R5", "R$35,00"),
            ("Refino único", "R$5,00"),
        ],
    },
    "builds": {
        "label": "Builds", "emoji": "🛠️",
        "itens": [
            ("Básica", "R$9,00"),
            ("Média", "R$14,00"),
            ("Excelente", "R$24,00"),
            ("Ajustes na build, sem farm", "R$5,00"),
        ],
        "nota": "Sem resina disponível na conta: taxa adicional de 15%.",
    },
    "manutencao": {
        "label": "Manutenção", "emoji": "🔧",
        "itens": [
            ("Diárias (por dia)", "R$1,20"),
            ("Pacote mensal de Diárias", "R$29,00"),
            ("Resinas (por dia)", "R$1,30"),
            ("Pacote mensal de Resinas", "R$29,00"),
            ("Diárias + Resinas (por dia)", "R$1,50"),
            ("Pacote mensal Diárias + Resinas", "R$34,00"),
            ("Reputação semanal", "R$4,00"),
        ],
    },
    "missoes": {
        "label": "Missões", "emoji": "📜",
        "itens": [
            ("Mundo Simples", "R$4,00"),
            ("Mundo Complexa", "R$9,00"),
            ("Lendária", "R$6,00"),
            ("Encontro", "R$9,00"),
            ("Arconte (por ato)", "R$9,00"),
            ("Cadeia dos Aranaras Completa", "R$79,00"),
            ("Aranaras", "R$55,00"),
            ("Ilha Tsurumi", "R$19,00"),
        ],
    },
    "eventos": {
        "label": "Eventos", "emoji": "🎉",
        "itens": [
            ("Comum", "R$11,00"),
            ("Complexo", "R$17,00"),
            ("Fontinalia Completo", "R$29,00"),
        ],
    },
    "tcg": {
        "label": "TCG", "emoji": "🎴",
        "itens": [
            ("Lv. 1 → 10", "R$34,00"),
            ("Lv. 2 → 10", "R$31,00"),
            ("Lv. 3 → 10", "R$27,00"),
            ("Lv. 4 → 10", "R$23,00"),
            ("Lv. 5 → 10", "R$19,00"),
            ("Lv. 6 → 10", "R$17,00"),
            ("Lv. 7 → 10", "R$14,00"),
            ("Lv. 8 → 10", "R$11,00"),
            ("Lv. 9 → 10", "R$7,00"),
        ],
    },
    "bule": {
        "label": "Bule de Relachá", "emoji": "🫖",
        "itens": [
            ("Por nível do Bule", "R$4,00"),
            ("Lv. 1 → 10", "R$45,00"),
        ],
    },
    "abismo": {
        "label": "End Game — Abismo", "emoji": "🏆",
        "itens": [
            ("Piso único", "R$3,00"),
            ("Andares 11 e 12", "R$7,00"),
            ("Andares 9, 10, 11 e 12", "R$15,00"),
            ("Andares 1 → 12", "R$25,00"),
        ],
    },
    "teatro": {
        "label": "End Game — Teatro", "emoji": "🎭",
        "itens": [
            ("Fácil", "R$5,00"),
            ("Médio", "R$8,00"),
            ("Difícil", "R$11,00"),
            ("Visionário", "R$14,00"),
            ("Lunar", "R$20,00"),
            ("Rastro", "R$3,00"),
        ],
    },
    "confronto": {
        "label": "Confronto Abissal", "emoji": "🌑",
        "itens": [
            ("Completo com a Skin", "R$14,00"),
            ("Até as Penas", "R$9,00"),
            ("Somente as Gemas", "R$7,00"),
        ],
    },
    "extras": {
        "label": "Extras", "emoji": "➕",
        "itens": [
            ("Flores de personagem (cada)", "R$0,15"),
            ("Lendas Locais (cada requisito)", "R$1,50"),
            ("Uma Lenda Local completa", "R$3,00"),
            ("Borboletas (cada)", "R$0,15"),
            ("Minérios (cada)", "R$0,25"),
        ],
    },
    "packs": {
        "label": "Packs Especiais", "emoji": "🎁",
        "itens": [
            ("Combo Vesna / Vodyanitsa — Upgrade Máximo", "R$49,00"),
        ],
        "nota": "Serviços Script. Consulte nossa equipe para contratar ou tirar dúvidas.",
    },
}


# ==================================================================
# CORES E CONSTANTES
# ==================================================================
COR_MANUAL = discord.Color.from_rgb(190, 160, 255)
COR_SCRIPT = discord.Color.from_rgb(255, 170, 90)
RODAPE = "୨୧・𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆 — Onde sua jornada começa. ᰔ"

TABELAS = {
    "manual": {"titulo": "📘 Manual", "servicos": SERVICOS_MANUAL, "cor": COR_MANUAL},
    "script": {"titulo": "⚡ Script", "servicos": SERVICOS_SCRIPT, "cor": COR_SCRIPT},
}


def _texto_itens(dados: dict) -> str:
    """Monta o texto da categoria (só os itens), sem repetir o título."""
    # Formato com subgrupos
    if "subgrupos" in dados:
        blocos = []
        for sub in dados["subgrupos"]:
            bloco = f"**{sub['titulo']}**\n"
            bloco += "\n".join(
                f"{label} — **{valor}**" for label, valor in sub["itens"]
            )
            blocos.append(bloco)
        texto = "\n\n".join(blocos)
    else:
        # Formato plano
        texto = "\n".join(
            f"**{label}** — **{valor}**" for label, valor in dados["itens"]
        )

    # Nota (letras miúdas) no final
    if "nota" in dados and dados["nota"]:
        texto += f"\n\n-# {dados['nota']}"

    return texto


def montar_embed_categoria(tipo: str, chave: str) -> discord.Embed:
    dados = TABELAS[tipo]["servicos"][chave]
    cor = TABELAS[tipo]["cor"]
    titulo_tipo = TABELAS[tipo]["titulo"]

    embed = discord.Embed(
        title=f"{dados['emoji']} {dados['label']} — {titulo_tipo}",
        description=_texto_itens(dados),
        color=cor,
    )
    embed.set_footer(text=RODAPE)
    return embed


# ==================================================================
# VIEW 1 — PAINEL DE PREÇOS (escolhe Manual ou Script)
# ==================================================================
class EscolhaTipoPrecosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(
        placeholder="Escolha o tipo de serviço...",
        min_values=1, max_values=1,
        custom_id="precos_escolha_tipo",
        options=[
            discord.SelectOption(label="Manual", value="manual",
                description="Serviço feito por um Farmer da equipe", emoji="📘"),
            discord.SelectOption(label="Script", value="script",
                description="Serviço automatizado / impulso", emoji="⚡"),
        ],
    )
    async def escolher(self, interaction: discord.Interaction, select: discord.ui.Select):
        tipo = select.values[0]
        servicos = TABELAS[tipo]["servicos"]
        cor = TABELAS[tipo]["cor"]
        titulo_tipo = TABELAS[tipo]["titulo"]

        linhas = [f"{d['emoji']} {d['label']}" for d in servicos.values()]
        descricao = (
            f"・𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆\n"
            f"**{titulo_tipo}**\n\n"
            "˖ ִֶָ Aqui você encontra nossa tabelinha de preços para os serviços "
            "de Genshin Impact!\n"
            "Cada pedido é tratado como uma nova jornada — feita com dedicação, "
            "segurança e carinho. ୨୧\n\n"
            "˚₊‧୨୧ 𝐄𝐬𝐜𝐨𝐥𝐡𝐚 𝐮𝐦𝐚 𝐜𝐚𝐭𝐞𝐠𝐨𝐫𝐢𝐚 𝐚𝐛𝐚𝐢𝐱𝐨 𝐩𝐚𝐫𝐚 𝐜𝐨𝐧𝐟𝐞𝐫𝐢𝐫 𝐨𝐬 𝐯𝐚𝐥𝐨𝐫𝐞𝐬!\n\n"
            + "\n".join(linhas)
            + "\n\n"
            "-# Os preços podem ser ajustados conforme a necessidade do serviço."
        )

        embed = discord.Embed(
            title=f"୨୧﹒𝑪𝒐𝒏𝒇𝒊𝒓𝒂 𝑵𝒐𝒔𝒔𝒐𝒔 𝑷𝒓𝒆𝒄̧𝒐𝒔 {titulo_tipo}! ୨୧",
            description=descricao,
            color=cor,
        )
        embed.set_footer(text=RODAPE)

        await interaction.response.send_message(
            embed=embed,
            view=MenuPrecosView(tipo=tipo),
            ephemeral=True,
        )


# ==================================================================
# VIEW 2 — MENU DE CATEGORIAS
# ==================================================================
class MenuPrecosView(discord.ui.View):
    def __init__(self, tipo: str):
        super().__init__(timeout=None)
        self.tipo = tipo
        servicos = TABELAS[tipo]["servicos"]

        select = discord.ui.Select(
            placeholder="Escolha uma categoria...",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(label=d["label"], value=chave, emoji=d["emoji"])
                for chave, d in servicos.items()
            ][:25],
            custom_id=f"precos_menu_{tipo}",
        )
        select.callback = self.selecionar
        self.add_item(select)

    async def selecionar(self, interaction: discord.Interaction):
        chave = interaction.data["values"][0]
        await interaction.response.send_message(
            embed=montar_embed_categoria(self.tipo, chave),
            view=VerOutraCategoriaView(tipo=self.tipo, chave_atual=chave),
            ephemeral=True,
        )


class VerOutraCategoriaView(discord.ui.View):
    def __init__(self, tipo: str, chave_atual: str):
        super().__init__(timeout=180)
        self.tipo = tipo
        self.chave_atual = chave_atual
        servicos = TABELAS[tipo]["servicos"]

        select = discord.ui.Select(
            placeholder="Ver outra categoria...",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(
                    label=d["label"], value=chave, emoji=d["emoji"],
                    default=(chave == chave_atual),
                )
                for chave, d in servicos.items()
            ][:25],
            custom_id=f"precos_ephemeral_{tipo}",
        )
        select.callback = self.trocar
        self.add_item(select)

    async def trocar(self, interaction: discord.Interaction):
        chave = interaction.data["values"][0]
        await interaction.response.edit_message(
            embed=montar_embed_categoria(self.tipo, chave),
            view=VerOutraCategoriaView(tipo=self.tipo, chave_atual=chave),
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
            title="୨୧﹒𝑪𝒐𝒏𝒇𝒊𝒓𝒂 𝑵𝒐𝒔𝒔𝒐𝒔 𝑷𝒓𝒆𝒄̧𝒐𝒔!﹒୨୧",
            description=(
                "﹒Escolha abaixo qual tipo de serviço você quer ver: "
                "**Manual** ou **Script**.﹒୨୧\n\n"
                "˚₊‧ ୨୧ Manual — serviços feitos por Farmers da equipe\n"
                "˚₊‧ ୨୧ Script — serviços automatizados\n\n"
            ),
            color=discord.Color.gold(),
        )
        embed.set_footer(text=RODAPE)
        await ctx.send(embed=embed, view=EscolhaTipoPrecosView())


async def setup(bot: commands.Bot):
    await bot.add_cog(Precos(bot))