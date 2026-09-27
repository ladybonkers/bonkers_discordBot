from __future__ import annotations

import os
import re
import asyncio
import traceback
import discord
from discord import ui
from discord.ext import commands

# Importa as tabelas de preços do precos.py
from cogs.precos import SERVICOS_MANUAL, SERVICOS_SCRIPT


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

DONA_LUMINE_ID = int(os.getenv("DONA_LUMINE_ID", "0"))
DONA_AETHER_ID = int(os.getenv("DONA_AETHER_ID", "0"))

LOGSTICKET_ID = int(os.getenv("LOGSTICKET_ID", "0"))

DESCONTO_FUNCIONARIO = 0.15
CHAVE_PIX = "melzinha.costaa.s@gmail.com"

COR_MANUAL = discord.Color.from_rgb(190, 160, 255)
COR_SCRIPT = discord.Color.from_rgb(255, 170, 90)


# ==================================================================
# HELPERS
# ==================================================================
def slugificar(texto: str) -> str:
    """Transforma '800 Gemas (5 giros)' em '800gemas'."""
    texto = texto.lower()
    texto = re.sub(r"\(.*?\)", "", texto)
    texto = re.sub(r"[^a-z0-9]+", "", texto)
    return texto[:30] or "servico"


def nome_canal_ticket(membro: discord.Member, tipo: str, item_label: str) -> str:
    """Formato: usuario-item-tipo (ex: jarvs09-800gemas-manual)."""
    usuario = re.sub(r"[^a-z0-9]+", "", membro.name.lower())[:20]
    item = slugificar(item_label)
    return f"{usuario}-{item}-{tipo}"


def valor_com_desconto(valor_str: str) -> str:
    """Recebe 'R$12,00' e devolve 'R$10,20' (valor - 15%)."""
    try:
        limpo = valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
        valor = float(limpo)
        com_desc = valor * (1 - DESCONTO_FUNCIONARIO)
        return f"R${com_desc:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, AttributeError):
        return valor_str


def eh_staff(membro: discord.Member) -> bool:
    if membro.guild_permissions.manage_channels or membro.guild_permissions.administrator:
        return True
    cargos_permitidos = {CARGO_STAFF_ID, CARGO_MANUAL_ID, CARGO_SCRIPT_ID} - {0}
    return any(r.id in cargos_permitidos for r in membro.roles)


def tabela_por_tipo(tipo: str) -> dict:
    return SERVICOS_MANUAL if tipo == "manual" else SERVICOS_SCRIPT


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
        nome_base = re.sub(r"[^a-z0-9]+", "", interaction.user.name.lower())[:20]
        existentes = [
            ch.mention for ch in guild.text_channels
            if ch.name.startswith(f"{nome_base}-")
        ]
        if existentes:
            await interaction.response.send_message(
                f"Você já tem ticket aberto: {', '.join(existentes)}",
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
        min_values=1, max_values=1,
        custom_id="escolha_tipo_pedido",
        options=[
            discord.SelectOption(label="Manual", value="manual",
                description="Farm, build, missão, sessão de personagem...", emoji="📘"),
            discord.SelectOption(label="Script", value="script",
                description="Serviço automatizado / impulso.", emoji="⚡"),
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

        servicos = tabela_por_tipo(tipo)

        select = discord.ui.Select(
            placeholder="Escolha a categoria do serviço...",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(label=d["label"], value=chave, emoji=d["emoji"])
                for chave, d in servicos.items()
            ][:25],
            custom_id="escolha_categoria_servico",
        )
        select.callback = self.escolher_categoria
        self.add_item(select)

    async def escolher_categoria(self, interaction: discord.Interaction):
        chave = interaction.data["values"][0]
        servicos = tabela_por_tipo(self.tipo)
        dados = servicos[chave]

        # 🔧 Suporta categorias com "subgrupos" (ex: gemas script)
        if "subgrupos" in dados:
            itens_planos = []
            for sub in dados["subgrupos"]:
                for label, valor in sub["itens"]:
                    itens_planos.append((f"{sub['titulo']} — {label}", valor))
        else:
            itens_planos = list(dados["itens"])

        opcoes_itens = [
            discord.SelectOption(
                label=label[:100],
                value=f"{chave}|{label}|{valor}",
                description=valor,
            )
            for label, valor in itens_planos[:25]
        ]

        select_itens = discord.ui.Select(
            placeholder="Escolha o serviço específico...",
            min_values=1, max_values=1,
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

            nome = nome_canal_ticket(autor, self.tipo, item_label)
            existente = discord.utils.get(guild.text_channels, name=nome)
            if existente:
                await interaction.edit_original_response(
                    content=f"Você já tem esse ticket aberto: {existente.mention}",
                    view=None,
                )
                return

            if self.tipo == "manual":
                categoria_id = CATEGORIA_MANUAL_ID or CATEGORIA_TICKETS_ID
                cargo_id = CARGO_MANUAL_ID or CARGO_STAFF_ID
                cor = COR_MANUAL
            else:
                categoria_id = CATEGORIA_SCRIPT_ID or CATEGORIA_TICKETS_ID
                cargo_id = CARGO_SCRIPT_ID or CARGO_STAFF_ID
                cor = COR_SCRIPT

            categoria = guild.get_channel(categoria_id)
            cargo = guild.get_role(cargo_id)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                autor: discord.PermissionOverwrite(
                    view_channel=True, send_messages=True, read_message_history=True,
                    attach_files=True, embed_links=True,
                ),
                guild.me: discord.PermissionOverwrite(
                    view_channel=True, send_messages=True, manage_channels=True,
                    manage_permissions=True, embed_links=True,
                ),
            }
            for role in guild.roles:
                if role != guild.default_role and (
                    role.permissions.administrator or role.permissions.manage_channels
                ):
                    overwrites[role] = discord.PermissionOverwrite(
                        view_channel=True, send_messages=True
                    )

            canal = await guild.create_text_channel(
                name=nome,
                category=categoria,
                overwrites=overwrites,
                topic=f"Ticket {self.tipo} — {item_label} — {item_valor}",
            )

            embed_ticket = discord.Embed(
                title="୨୧・𝑻𝒊𝒄𝒌𝒆𝒕 𝑨𝒃𝒆𝒓𝒕𝒐・୨୧",
                description=(
                    f"𓆩♡𓆪・Olá {autor.mention}! Seu ticket foi criado com sucesso.\n\n"
                    f"**📍 Serviço escolhido**\n"
                    f"{item_label}\n\n"
                    f"**💰 Valor**\n"
                    f"**{item_valor}**\n\n"
                    "**💳 Pagamento via PIX**\n"
                    f"`{CHAVE_PIX}`\n"
                    "-# Envie o comprovante aqui no ticket após o pagamento.\n\n"
                    "**📜 Sobre reembolsos**\n"
                    "-# • Cancelamentos antes do início do serviço podem ser aceitos, "
                    "com desconto de 20% do valor pago referente aos custos operacionais.\n"
                    "-# • Após o início do serviço, o reembolso será calculado de acordo "
                    "com o progresso realizado.\n"
                    "-# • Reembolso integral apenas quando a equipe não puder concluir "
                    "o serviço por responsabilidade da loja.\n\n"
                    "˚₊‧୨୧ **O pagamento deve ser feito antes do serviço começar.** "
                    "Assim que o comprovante for enviado, a equipe liberará o pedido "
                    "para um Farmer assumir.\n\n"
                    "-# A equipe vai te atender em breve. ♡"
                ),
                color=cor,
            )
            embed_ticket.set_footer(
                text="Traveler Store ✦ Onde sua jornada começa."
            )

            view_ticket = TicketAbertoView()
            try:
                await canal.send(embed=embed_ticket, view=view_ticket)
            except discord.HTTPException as e:
                print(f"[TICKET] Falha ao enviar embed: {e}")
                traceback.print_exc()

            await interaction.edit_original_response(
                content=f"✅ Ticket criado: {canal.mention}",
                view=None,
            )

        except Exception:
            print("[TICKET] Erro geral ao criar ticket:")
            traceback.print_exc()
            try:
                await interaction.edit_original_response(
                    content="❌ Erro ao criar ticket. Avise a staff.", view=None,
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
            await canal.set_permissions(interaction.guild.default_role, view_channel=False)
        except discord.HTTPException as e:
            print(f"[TICKET] Erro ao preparar fechamento: {e}")
        await asyncio.sleep(5)
        try:
            await canal.delete()
        except discord.HTTPException as e:
            print(f"[TICKET] Erro ao deletar: {e}")

    @discord.ui.button(
        label="Adicionar Membro",
        style=discord.ButtonStyle.secondary,
        emoji="👥",
        custom_id="adicionar_membro_ticket",
    )
    async def adicionar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not eh_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas a **equipe** pode adicionar membros.", ephemeral=True,
            )
            return
        await interaction.response.send_modal(AdicionarMembroModal())


# ==================================================================
# 6) MODAL — Adicionar membro
# ==================================================================
class AdicionarMembroModal(discord.ui.Modal, title="Adicionar membro ao ticket"):
    membro_id = discord.ui.TextInput(
        label="ID do membro",
        placeholder="Ex: 123456789012345678",
        required=True, max_length=25,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            membro = interaction.guild.get_member(int(self.membro_id.value))
            if membro is None:
                membro = await interaction.guild.fetch_member(int(self.membro_id.value))
        except (ValueError, discord.NotFound):
            await interaction.response.send_message(
                "❌ ID inválido ou membro não encontrado.", ephemeral=True,
            )
            return

        try:
            await interaction.channel.set_permissions(
                membro, view_channel=True, send_messages=True,
                read_message_history=True, attach_files=True, embed_links=True,
            )
            await interaction.response.send_message(
                f"✅ {membro.mention} foi adicionado por {interaction.user.mention}."
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erro: {e}", ephemeral=True)


# ==================================================================
# 7) VIEW DA NOTIFICAÇÃO AOS FARMERS
# ==================================================================
class NotificacaoStaffView(discord.ui.View):
    def __init__(self, canal_ticket_id: int, tipo: str, item_label: str = ""):
        super().__init__(timeout=None)
        self.canal_ticket_id = canal_ticket_id
        self.tipo = tipo
        self.item_label = item_label

    @discord.ui.button(
        label="Assumir Pedido",
        style=discord.ButtonStyle.success,
        emoji="✋",
        custom_id="assumir_pedido",
    )
    async def assumir(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not eh_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Apenas membros da **equipe** podem assumir pedidos.", ephemeral=True,
            )
            return

        guild = interaction.guild
        canal = guild.get_channel(self.canal_ticket_id)

        # Canal sumiu (ticket fechado)
        if canal is None:
            button.disabled = True
            button.label = "Ticket fechado"
            button.style = discord.ButtonStyle.secondary
            try:
                await interaction.message.edit(view=self)
            except discord.HTTPException:
                pass
            await interaction.response.send_message(
                "❌ Este ticket já foi fechado.", ephemeral=True,
            )
            return

        topico = canal.topic or ""

        # Já assumido → deixa cinza e avisa (sem erro)
        if "Assumido por:" in topico:
            responsavel_id = topico.split("Assumido por:")[-1].split("|")[0].strip()
            button.disabled = True
            button.label = f"Assumido por <@{responsavel_id}>"
            button.style = discord.ButtonStyle.secondary
            try:
                await interaction.message.edit(view=self)
            except discord.HTTPException:
                pass
            await interaction.response.send_message(
                f"⚠️ Este pedido já foi assumido por <@{responsavel_id}>.",
                ephemeral=True,
            )
            return

        # ==== ASSUME PELA PRIMEIRA VEZ ====

        await interaction.response.send_message(
            f"✅ Você assumiu o pedido! Acesse {canal.mention}",
            ephemeral=True,
        )

        try:
            await canal.set_permissions(
                interaction.user, view_channel=True, send_messages=True,
                read_message_history=True, attach_files=True, embed_links=True,
            )
        except discord.HTTPException as e:
            print(f"[TICKET] Erro ao dar acesso: {e}")

        try:
            await canal.edit(topic=f"{topico} | Assumido por: {interaction.user.id}")
        except discord.HTTPException:
            pass

        button.disabled = True
        button.label = f"Assumido por {interaction.user.display_name}"
        button.style = discord.ButtonStyle.secondary

        try:
            await interaction.message.edit(view=self)
        except discord.HTTPException as e:
            print(f"[TICKET] Erro ao editar botão: {e}")

        try:
            await canal.send(
                f"✋ {interaction.user.mention} assumiu este pedido e cuidará do atendimento!"
            )
        except discord.HTTPException as e:
            print(f"[TICKET] Erro ao avisar no ticket: {e}")

        await self._avisar_donos(guild, canal, interaction.user)

    async def _avisar_donos(self, guild, canal, farmer: discord.Member):
        """Tenta DM pros donos. Se falhar, posta no canal de log."""
        texto = (
            f"✋ **Novo pedido assumido!**\n\n"
            f"**Ticket:** `{canal.name}`\n"
            f"**Assumido por:** {farmer.mention} (`{farmer.id}`)\n"
            f"**Link:** {canal.jump_url}"
        )

        donos_ids = [i for i in (DONA_LUMINE_ID, DONA_AETHER_ID) if i]
        algum_dm_ok = False

        for dono_id in donos_ids:
            try:
                dono = guild.get_member(dono_id) or await guild.fetch_member(dono_id)
            except (discord.NotFound, discord.HTTPException):
                continue

            try:
                await dono.send(texto)
                algum_dm_ok = True
            except discord.Forbidden:
                print(f"[TICKET] DM fechada pra {dono.name}")
            except Exception as e:
                print(f"[TICKET] Erro ao mandar DM: {e}")

        if not algum_dm_ok and LOGSTICKET_ID:
            canal_log = guild.get_channel(LOGSTICKET_ID)
            if canal_log:
                try:
                    await canal_log.send(texto)
                except discord.HTTPException as e:
                    print(f"[TICKET] Erro ao postar no canal de log: {e}")


# ==================================================================
# 8) COG
# ==================================================================
class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------------- !painel ----------------
    @commands.command(name="painel")
    @commands.has_permissions(manage_guild=True)
    async def painel(self, ctx: commands.Context):
        embed = discord.Embed(
            title="୨୧﹒ 𝑨𝒃𝒓𝒂 𝒔𝒆𝒖 𝑻𝒊𝒄𝒌𝒆𝒕! ﹒୨୧",
            description=(
                "˖ ִֶָ  Pronto pra começar sua próxima aventura? "
                "Escolha o tipo de pedido e nós cuidamos do resto. ୨୧\n\n"
                "˚₊‧ ୨୧ **Tipos de pedido disponíveis:**\n"
                "`📘` 𝑴𝒂𝒏𝒖𝒂𝒍 — farm, build, missão, sessão de personagem...\n"
                "`⚡` 𝑺𝒄𝒓𝒊𝒑𝒕 — serviço automatizado \n\n"
                "**₊‧ ୨୧ Diferenciais:**\n"
                "・ Entrega rápida\n"
                "・ Atendimento exclusivo via ticket\n"
                "・ Equipe dedicada\n\n"
                "-# Ao abrir um ticket, você concorda com nossos termos de serviço."
            ),
            color=discord.Color.from_rgb(150, 120, 220),
        )
        embed.set_footer(text="୨୧・𝑻𝒓𝒂𝒗𝒆𝒍𝒆𝒓 𝑺𝒕𝒐𝒓𝒆 — Onde sua jornada começa. ᰔ")
        await ctx.send(embed=embed, view=PainelTicketView())

    # ---------------- !add ----------------
    @commands.command(name="add")
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx: commands.Context, membro: discord.Member):
        if not eh_staff(ctx.author):
            await ctx.reply("❌ Apenas a **equipe** pode adicionar membros.")
            return
        try:
            await ctx.channel.set_permissions(
                membro, view_channel=True, send_messages=True,
                read_message_history=True, attach_files=True, embed_links=True,
            )
            await ctx.reply(f"✅ {membro.mention} foi adicionado por {ctx.author.mention}.")
        except discord.HTTPException as e:
            await ctx.reply(f"❌ Erro: {e}")

    # ---------------- !pedidomanual ----------------
    @commands.command(name="pedidomanual")
    @commands.has_permissions(manage_channels=True)
    async def pedidomanual(self, ctx: commands.Context):
        await self._enviar_pedido(ctx, tipo="manual")

    # ---------------- !pedidoscript ----------------
    @commands.command(name="pedidoscript")
    @commands.has_permissions(manage_channels=True)
    async def pedidoscript(self, ctx: commands.Context):
        await self._enviar_pedido(ctx, tipo="script")

    async def _enviar_pedido(self, ctx: commands.Context, tipo: str):
        topico = ctx.channel.topic or ""
        if not topico.startswith("Ticket "):
            await ctx.reply(
                "❌ Este comando só pode ser usado dentro de um canal de ticket."
            )
            return

        if not eh_staff(ctx.author):
            await ctx.reply("❌ Apenas a **equipe** pode liberar pedidos pros farmers.")
            return

        partes = topico.split(" — ")
        if len(partes) < 3:
            await ctx.reply("❌ Não consegui ler as informações do ticket.")
            return

        tipo_do_topico = partes[0].replace("Ticket ", "").strip()
        item_label = partes[1].strip()
        item_valor = partes[2].strip()

        if tipo_do_topico != tipo:
            await ctx.reply(
                f"❌ Este ticket é **{tipo_do_topico}**. Use "
                f"`!pedido{tipo_do_topico}` em vez disso."
            )
            return

        canal_notif_id = CANAL_NOTIF_MANUAL_ID if tipo == "manual" else CANAL_NOTIF_SCRIPT_ID
        if not canal_notif_id:
            await ctx.reply(f"❌ CANAL_NOTIF_{tipo.upper()}_ID não configurado no .env")
            return

        canal_notif = ctx.guild.get_channel(canal_notif_id)
        if canal_notif is None:
            await ctx.reply(f"❌ Canal de notificação não encontrado: `{canal_notif_id}`")
            return

        cargo_farmer = ctx.guild.get_role(CARGO_FARMER_ID)
        mencao = cargo_farmer.mention if cargo_farmer else ""

        emoji = "📘" if tipo == "manual" else "⚡"
        valor_func = valor_com_desconto(item_valor)

        # Pega o dono do canal (cliente)
        dono_ticket = None
        for membro_id, ov in ctx.channel.overwrites.items():
            if isinstance(membro_id, discord.Member) and ov.view_channel:
                if not membro_id.bot and not eh_staff(membro_id):
                    dono_ticket = membro_id
                    break

        cliente_txt = dono_ticket.mention if dono_ticket else "ver no ticket"

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
                f"{cliente_txt}\n\n"
                "**🎫 Ticket**\n"
                f"{ctx.channel.mention}"
            ),
            color=COR_MANUAL if tipo == "manual" else COR_SCRIPT,
        )
        embed.set_footer(
            text=f"✋ Clique em Assumir pra pegar o pedido • Valor já com desconto de {int(DESCONTO_FUNCIONARIO*100)}%"
        )

        view = NotificacaoStaffView(
            canal_ticket_id=ctx.channel.id,
            tipo=tipo,
            item_label=item_label,
        )

        try:
            if mencao:
                await canal_notif.send(content=mencao, embed=embed, view=view)
            else:
                await canal_notif.send(embed=embed, view=view)
            await ctx.reply(f"✅ Pedido enviado para {canal_notif.mention}!")
        except discord.HTTPException as e:
            await ctx.reply(f"❌ Erro ao enviar: {e}")
            traceback.print_exc()

    # ---------------- AO LIGAR: ajusta botões antigos ----------------
    @commands.Cog.listener()
    async def on_ready(self):
        """Varre notificações antigas e deixa cinza os botões já assumidos."""
        print("[TICKET] Verificando notificações antigas...")

        canais_notif = []
        for cid in (CANAL_NOTIF_MANUAL_ID, CANAL_NOTIF_SCRIPT_ID):
            if cid:
                ch = self.bot.get_channel(cid)
                if ch:
                    canais_notif.append(ch)

        total_ajustados = 0
        for canal in canais_notif:
            try:
                async for msg in canal.history(limit=200):
                    if not msg.embeds or msg.author.id != self.bot.user.id:
                        continue

                    embed = msg.embeds[0]
                    if not embed.title or "Novo Pedido" not in embed.title:
                        continue

                    # Descobre o canal do ticket pelo embed
                    canal_ticket = None
                    for field in embed.fields:
                        if "Ticket" in field.name:
                            match = re.search(r"<#(\d+)>", field.value)
                            if match:
                                canal_ticket = self.bot.get_channel(int(match.group(1)))
                                break

                    if canal_ticket is None:
                        continue

                    topico = canal_ticket.topic or ""
                    if "Assumido por:" not in topico:
                        continue

                    responsavel_id = topico.split("Assumido por:")[-1].split("|")[0].strip()
                    try:
                        responsavel = canal_ticket.guild.get_member(int(responsavel_id))
                    except ValueError:
                        responsavel = None
                    nome_resp = responsavel.display_name if responsavel else "alguém"

                    # Verifica se já tá cinza
                    if msg.components and msg.components[0].children:
                        botao = msg.components[0].children[0]
                        if botao.disabled:
                            continue

                    view = NotificacaoStaffView(
                        canal_ticket_id=canal_ticket.id,
                        tipo="manual" if "Manual" in embed.title else "script",
                    )
                    botao_novo = view.children[0]
                    botao_novo.disabled = True
                    botao_novo.label = f"Assumido por {nome_resp}"
                    botao_novo.style = discord.ButtonStyle.secondary

                    try:
                        await msg.edit(view=view)
                        total_ajustados += 1
                    except discord.HTTPException as e:
                        print(f"[TICKET] Erro ao ajustar msg: {e}")

            except discord.HTTPException as e:
                print(f"[TICKET] Erro ao varrer {canal.name}: {e}")

        print(f"[TICKET] {total_ajustados} notificações ajustadas.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))