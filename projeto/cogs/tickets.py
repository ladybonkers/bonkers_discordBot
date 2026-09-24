from __future__ import annotations

import os
import asyncio
import traceback
import discord
from discord import ui
from discord.ext import commands

# ---- IDs do .env ----
CATEGORIA_TICKETS_ID = int(os.getenv("CATEGORIA_TICKETS_ID", "0"))
CARGO_STAFF_ID = int(os.getenv("CARGO_STAFF_ID", "0"))

CATEGORIA_MANUAL_ID = int(os.getenv("CATEGORIA_MANUAL_ID", "0"))
CATEGORIA_SCRIPT_ID = int(os.getenv("CATEGORIA_SCRIPT_ID", "0"))
CARGO_MANUAL_ID = int(os.getenv("CARGO_MANUAL_ID", "0"))
CARGO_SCRIPT_ID = int(os.getenv("CARGO_SCRIPT_ID", "0"))

CANAL_NOTIF_MANUAL_ID = int(os.getenv("CANAL_NOTIF_MANUAL_ID", "0"))
CANAL_NOTIF_SCRIPT_ID = int(os.getenv("CANAL_NOTIF_SCRIPT_ID", "0"))
CARGO_FARMER_ID = int(os.getenv("CARGO_FARMER_ID", "0"))

# Desconto aplicado em cima do valor cheio (15% que fica pra loja)
DESCONTO_FUNCIONARIO = 0.15

COR_MANUAL = discord.Color.from_rgb(190, 160, 255)
COR_SCRIPT = discord.Color.from_rgb(255, 170, 90)


# ==================================================================
# SERVIÇOS — categorias + itens com valor CHEIO (o que o cliente paga)
# ==================================================================
SERVICOS: dict[str, dict] = {
    "gemas": {
        "label": "Gemas", "emoji": "💎",
        "itens": [
            ("800 Gemas (5 giros)", "R$9,00"),
            ("1.600 Gemas (10 giros)", "R$18,00"),
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
    },
    "manutencao": {
        "label": "Manutenção", "emoji": "🔧",
        "itens": [
            ("Diárias (por dia)", "R$1,20"),
            ("Pacote mensal de Diárias", "R$30,00"),
            ("Resinas (por dia)", "R$1,30"),
            ("Pacote mensal de Resinas", "R$30,00"),
            ("Diárias + Resinas (por dia)", "R$1,50"),
            ("Pacote mensal de Diárias + Resinas", "R$35,00"),
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
    },
}


# ==================================================================
# HELPERS
# ==================================================================
def nome_canal_ticket(membro: discord.Member, tipo: str) -> str:
    return f"{tipo}-{membro.name}".lower().replace(" ", "-")


def valor_com_desconto(valor_str: str) -> str:
    """Recebe 'R$12,00' e devolve 'R$10,20' (valor - 15%)."""
    try:
        limpo = valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
        valor = float(limpo)
        com_desc = valor * (1 - DESCONTO_FUNCIONARIO)
        return f"R${com_desc:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, AttributeError):
        return valor_str  # fallback: devolve como veio


def eh_staff(membro: discord.Member) -> bool:
    """Admin OU tem algum cargo configurado como staff."""
    if membro.guild_permissions.manage_channels or membro.guild_permissions.administrator:
        return True
    cargos_permitidos = {CARGO_STAFF_ID, CARGO_MANUAL_ID, CARGO_SCRIPT_ID} - {0}
    if any(r.id in cargos_permitidos for r in membro.roles):
        return True
    return False


# ==================================================================
# 1) PAINEL PRINCIPAL
# ==================================================================
class PainelTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Abrir Ticket de Compra",
        style=discord.ButtonStyle.success,
        emoji="🛒",
        custom_id="abrir_ticket",
    )
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        tipos_existentes = []
        for tipo in ("manual", "script"):
            ch = discord.utils.get(
                guild.text_channels, name=nome_canal_ticket(interaction.user, tipo)
            )
            if ch:
                tipos_existentes.append(ch.mention)

        if tipos_existentes:
            await interaction.response.send_message(
                f"Você já tem ticket aberto: {', '.join(tipos_existentes)}",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Escolha o tipo do seu pedido:",
            view=EscolhaTipoView(),
            ephemeral=True,
        )


# ==================================================================
# 2) ESCOLHA DO TIPO
# ==================================================================
class EscolhaTipoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(
        placeholder="Escolha o tipo de pedido...",
        min_values=1,
        max_values=1,
        custom_id="escolha_tipo_pedido",
        options=[
            discord.SelectOption(
                label="Manual", value="manual",
                description="Farm, build, missão, sessão de personagem...",
                emoji="📘",
            ),
            discord.SelectOption(
                label="Script", value="script",
                description="Serviço automatizado / impulso.",
                emoji="⚡",
            ),
        ],
    )
    async def escolher(self, interaction: discord.Interaction, select: discord.ui.Select):
        tipo = select.values[0]
        await interaction.response.edit_message(
            content=f"Tipo escolhido: **{tipo.capitalize()}**. Agora escolha a categoria:",
            view=EscolhaCategoriaView(tipo=tipo),
        )


# ==================================================================
# 3) ESCOLHA DA CATEGORIA
# ==================================================================
class EscolhaCategoriaView(discord.ui.View):
    def __init__(self, tipo: str):
        super().__init__(timeout=180)
        self.tipo = tipo

        select = discord.ui.Select(
            placeholder="Escolha a categoria do serviço...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=dados["label"],
                    value=chave,
                    emoji=dados["emoji"],
                )
                for chave, dados in SERVICOS.items()
            ][:25],
            custom_id="escolha_categoria_servico",
        )
        select.callback = self.escolher_categoria
        self.add_item(select)

    async def escolher_categoria(self, interaction: discord.Interaction):
        chave = interaction.data["values"][0]
        dados = SERVICOS[chave]

        opcoes_itens = [
            discord.SelectOption(
                label=label[:100],
                value=f"{chave}|{label}|{valor}",
                description=valor,
            )
            for label, valor in dados["itens"][:25]
        ]

        select_itens = discord.ui.Select(
            placeholder="Escolha o serviço específico...",
            min_values=1,
            max_values=1,
            options=opcoes_itens,
            custom_id="escolha_item_servico",
        )
        select_itens.callback = EscolhaItemCallback(tipo=self.tipo).callback

        view = discord.ui.View(timeout=180)
        view.add_item(select_itens)

        await interaction.response.edit_message(
            content=f"Categoria: **{dados['emoji']} {dados['label']}**. Agora escolha o item:",
            view=view,
        )


# ==================================================================
# 4) CALLBACK DO ITEM → CRIA TICKET
# ==================================================================
class EscolhaItemCallback:
    def __init__(self, tipo: str):
        self.tipo = tipo

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            chave, item_label, item_valor = interaction.data["values"][0].split("|")
            autor = interaction.user
            guild = interaction.guild

            nome = nome_canal_ticket(autor, self.tipo)
            existente = discord.utils.get(guild.text_channels, name=nome)
            if existente:
                await interaction.edit_original_response(
                    content=f"Você já tem um ticket **{self.tipo}** aberto: {existente.mention}",
                    view=None,
                )
                return

            if self.tipo == "manual":
                categoria_id = CATEGORIA_MANUAL_ID or CATEGORIA_TICKETS_ID
                cargo_id = CARGO_MANUAL_ID or CARGO_STAFF_ID
                canal_notif_id = CANAL_NOTIF_MANUAL_ID
                cor = COR_MANUAL
            else:
                categoria_id = CATEGORIA_SCRIPT_ID or CATEGORIA_TICKETS_ID
                cargo_id = CARGO_SCRIPT_ID or CARGO_STAFF_ID
                canal_notif_id = CANAL_NOTIF_SCRIPT_ID
                cor = COR_SCRIPT

            categoria = guild.get_channel(categoria_id)
            cargo = guild.get_role(cargo_id)

            # ⚠️ IMPORTANTE: os funcionários NÃO têm acesso de primeira.
            # Só o cliente + o bot + cargos de adm/mod (que são admin do server).
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                autor: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    attach_files=True,
                    embed_links=True,
                ),
                guild.me: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_channels=True,
                    manage_permissions=True,
                    embed_links=True,
                ),
            }
            # Admin/mod do server (que têm manage_channels) enxergam por padrão?
            # Não automaticamente. Vamos dar acesso a cargos com permissão de admin:
            for role in guild.roles:
                if role.permissions.administrator or role.permissions.manage_channels:
                    if role != guild.default_role:
                        overwrites[role] = discord.PermissionOverwrite(
                            view_channel=True, send_messages=True
                        )

            canal = await guild.create_text_channel(
                name=nome,
                category=categoria,
                overwrites=overwrites,
                topic=f"Ticket {self.tipo} — {item_label} | Preço cheio: {item_valor}",
            )

            # -------- Mensagem DENTRO do ticket (cliente vê valor CHEIO) --------
            embed_ticket = discord.Embed(
                title="🔒 Atendimento em andamento",
                description=(
                    f"Olá {autor.mention}! Seu ticket foi aberto.\n\n"
                    f"**Serviço escolhido:** {item_label}\n"
                    f"**Valor:** {item_valor}\n\n"
                    "Aguarde um membro da equipe te atender. Quando tudo "
                    "estiver resolvido, a **equipe** pode fechar o ticket "
                    "pelo botão abaixo."
                ),
                color=cor,
            )
            embed_ticket.set_footer(text="Traveler Store ✦ Todos os direitos reservados.")

            view_ticket = TicketAbertoView()
            try:
                await canal.send(embed=embed_ticket, view=view_ticket)
            except discord.HTTPException as e:
                print(f"[TICKET] Falha ao enviar embed dentro do ticket: {e}")
                traceback.print_exc()

            # -------- Notificação pra staff (valor COM desconto) --------
            await notificar_staff(
                guild=guild,
                tipo=self.tipo,
                autor=autor,
                canal_ticket=canal,
                canal_notif_id=canal_notif_id,
                item_label=item_label,
                item_valor=item_valor,
            )

            await interaction.edit_original_response(
                content=f"✅ Ticket criado: {canal.mention}",
                view=None,
            )

        except Exception:
            print("[TICKET] Erro geral ao criar ticket:")
            traceback.print_exc()
            try:
                await interaction.edit_original_response(
                    content="❌ Erro ao criar ticket. Avise a staff.",
                    view=None,
                )
            except Exception:
                pass


# ==================================================================
# 5) VIEW DENTRO DO TICKET — Fechar + Adicionar membro
# ==================================================================
class TicketAbertoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fechar Ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒",
        custom_id="fechar_ticket",
    )
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not eh_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas membros da **equipe** podem fechar este ticket.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message("🔒 Fechando ticket em 5 segundos...")
        canal = interaction.channel
        try:
            await canal.edit(name=f"fechado-{canal.name}")
            await canal.set_permissions(
                interaction.guild.default_role, view_channel=False
            )
        except discord.HTTPException as e:
            print(f"[TICKET] Erro ao preparar fechamento: {e}")
        await asyncio.sleep(5)
        try:
            await canal.delete()
        except discord.HTTPException as e:
            print(f"[TICKET] Erro ao deletar canal: {e}")

    @discord.ui.button(
        label="Adicionar Membro",
        style=discord.ButtonStyle.secondary,
        emoji="👥",
        custom_id="adicionar_membro_ticket",
    )
    async def adicionar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not eh_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a **equipe** pode adicionar membros.",
                ephemeral=True,
            )
            return

        await interaction.response.send_modal(AdicionarMembroModal())


# ==================================================================
# 6) COMANDO !add (dentro do ticket)
# ==================================================================
class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="painel")
    @commands.has_permissions(manage_guild=True)
    async def painel(self, ctx: commands.Context):
        embed = discord.Embed(
            title="୨୧﹒𓂃 𝑨𝒃𝒓𝒂 𝒔𝒆𝒖 𝑻𝒊𝒄𝒌𝒆𝒕! 𓂃﹒୨୧",
            description=(
                "𓆩♡𓆪・𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆\n\n"
                "𓂃 ࣪˖ ִֶָ Pronto pra começar sua próxima aventura? "
                "Escolha o tipo de pedido e nós cuidamos do resto. ୨୧\n\n"
                "˚₊‧୨୧ **Tipos de pedido disponíveis:**\n"
                "𓂃♡ 📘 𝑴𝒂𝒏𝒖𝒂𝒍 — farm, build, missão, sessão de personagem...\n"
                "𓂃♡ ⚡ 𝑺𝒄𝒓𝒊𝒑𝒕 — serviço automatizado / impulso\n\n"
                "**Diferenciais:**\n"
                "・ Entrega rápida\n"
                "・ Atendimento exclusivo via ticket\n"
                "・ Equipe dedicada\n\n"
                "-# Ao abrir um ticket, você concorda com nossos termos de serviço."
            ),
            color=discord.Color.from_rgb(150, 120, 220),
        )
        embed.set_footer(
            text="୨୨・𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆 — Onde sua jornada começa. ᰔ"
        )
        await ctx.send(embed=embed, view=PainelTicketView())

    # ---------------- !add ----------------
    @commands.command(name="add")
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx: commands.Context, membro: discord.Member):
        """Adiciona um membro ao ticket atual. Use dentro do canal do ticket."""
        if not eh_staff(ctx.author):
            await ctx.reply("❌ Apenas a **equipe** pode adicionar membros.")
            return

        try:
            await ctx.channel.set_permissions(
                membro,
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True,
            )
            await ctx.reply(
                f"✅ {membro.mention} foi adicionado ao ticket por {ctx.author.mention}."
            )
        except discord.HTTPException as e:
            await ctx.reply(f"❌ Erro ao adicionar: {e}")


# ==================================================================
# 7) MODAL — Adicionar membro
# ==================================================================
class AdicionarMembroModal(discord.ui.Modal, title="Adicionar membro ao ticket"):
    membro_id = discord.ui.TextInput(
        label="ID do membro",
        placeholder="Ex: 123456789012345678",
        required=True,
        max_length=25,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            membro = interaction.guild.get_member(int(self.membro_id.value))
            if membro is None:
                membro = await interaction.guild.fetch_member(int(self.membro_id.value))
        except (ValueError, discord.NotFound):
            await interaction.response.send_message(
                "❌ ID inválido ou membro não encontrado.", ephemeral=True
            )
            return

        try:
            await interaction.channel.set_permissions(
                membro,
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True,
            )
            await interaction.response.send_message(
                f"✅ {membro.mention} foi adicionado ao ticket por {interaction.user.mention}."
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"❌ Erro ao adicionar: {e}", ephemeral=True
            )


# ==================================================================
# 8) NOTIFICAÇÃO PRA STAFF — com botão Assumir
# ==================================================================
class NotificacaoStaffView(discord.ui.View):
    """View com botão Assumir + Fechar, anexada à notificação do canal da staff."""

    def __init__(self, canal_ticket_id: int, tipo: str):
        super().__init__(timeout=None)
        self.canal_ticket_id = canal_ticket_id
        self.tipo = tipo

    @discord.ui.button(
        label="Assumir Pedido",
        style=discord.ButtonStyle.success,
        emoji="✋",
        custom_id="assumir_pedido",
    )
    async def assumir(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not eh_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas membros da **equipe** podem assumir pedidos.",
                ephemeral=True,
            )
            return

        guild = interaction.guild
        canal = guild.get_channel(self.canal_ticket_id)
        if canal is None:
            await interaction.response.send_message(
                "❌ Não consegui encontrar o canal do ticket. Ele pode ter sido fechado.",
                ephemeral=True,
            )
            return

        topico = canal.topic or ""
        if "Assumido por:" in topico:
            responsavel_id = topico.split("Assumido por:")[-1].split("|")[0].strip()
            await interaction.response.send_message(
                f"❌ Este pedido já foi assumido por <@{responsavel_id}>.",
                ephemeral=True,
            )
            return

        # 1) Dá permissão ao funcionário no canal do ticket
        try:
            await canal.set_permissions(
                interaction.user,
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True,
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"❌ Erro ao dar acesso ao ticket: {e}", ephemeral=True
            )
            return

        # 2) Marca no tópico
        try:
            await canal.edit(topic=f"{topico} | Assumido por: {interaction.user.id}")
        except discord.HTTPException:
            pass

        # 3) Desabilita o botão + muda aparência
        button.disabled = True
        button.label = f"Assumido por {interaction.user.display_name}"
        button.style = discord.ButtonStyle.secondary

        # 4) Avisa no canal do ticket
        try:
            await canal.send(
                f"✋ {interaction.user.mention} assumiu este pedido e cuidará do atendimento!"
            )
        except discord.HTTPException:
            pass

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            f"✅ Você assumiu o pedido! Acesse {canal.mention}",
            ephemeral=True,
        )


async def notificar_staff(
    guild: discord.Guild,
    tipo: str,
    autor: discord.Member,
    canal_ticket: discord.TextChannel,
    canal_notif_id: int,
    item_label: str,
    item_valor: str,
):
    if not canal_notif_id:
        print("[TICKET] CANAL_NOTIF_*_ID não configurado no .env")
        return

    canal_notif = guild.get_channel(canal_notif_id)
    if canal_notif is None:
        print(f"[TICKET] Canal de notificação não encontrado: {canal_notif_id}")
        return

    cargo_farmer = guild.get_role(CARGO_FARMER_ID)
    mencao = cargo_farmer.mention if cargo_farmer else ""

    emoji = "📘" if tipo == "manual" else "⚡"
    valor_func = valor_com_desconto(item_valor)

    embed = discord.Embed(
        title=f"✦ Novo Pedido — {emoji} {tipo.capitalize()}",
        description=(
            "Um novo serviço foi publicado! Confira as informações abaixo:\n\n"
            "**📍 Serviço e Jogo**\n"
            f"{item_label}\n\n"
            "**💰 Valor (líquido pro funcionário)**\n"
            f"**{valor_func}**\n\n"
            "**⏳ Prazo**\n"
            "-# a combinar no ticket\n\n"
            "**👤 Cliente**\n"
            f"{autor.mention} (`{autor.id}`)\n\n"
            "**🎫 Ticket**\n"
            f"{canal_ticket.mention}"
        ),
        color=COR_MANUAL if tipo == "manual" else COR_SCRIPT,
    )
    embed.set_footer(
        text=f"✋ Clique em Assumir pra pegar o pedido • Valor já com desconto de {int(DESCONTO_FUNCIONARIO*100)}%"
    )

    view = NotificacaoStaffView(canal_ticket_id=canal_ticket.id, tipo=tipo)

    try:
        if mencao:
            await canal_notif.send(content=mencao, embed=embed, view=view)
        else:
            await canal_notif.send(embed=embed, view=view)
    except discord.HTTPException as e:
        print(f"[TICKET] Erro ao enviar notificação: {e}")
        traceback.print_exc()


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))