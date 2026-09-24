from __future__ import annotations

import os
import discord


def montar_embed(
    titulo: str,
    texto: str,
    cor: discord.Color = discord.Color.blurple(),
    rodape: str | None = None,
    banner_url: str | None = None,
    banner_path: str | None = None,
) -> tuple[discord.Embed, discord.File | None]:
    """Cria um embed padrão. Retorna (embed, arquivo)."""
    embed = discord.Embed(description=f"### {titulo}\n\n{texto}", color=cor)
    if rodape:
        embed.set_footer(text=rodape)

    arquivo = None
    if banner_path:
        nome = os.path.basename(banner_path)
        arquivo = discord.File(banner_path, filename=nome)
        embed.set_image(url=f"attachment://{nome}")
    elif banner_url:
        embed.set_image(url=banner_url)

    return embed, arquivo


async def enviar_embed(
    destino,
    titulo: str,
    texto: str,
    cor: discord.Color = discord.Color.blurple(),
    rodape: str | None = None,
    banner_url: str | None = None,
    banner_path: str | None = None,
    content: str | None = None,
):
    """Envia um embed tratando banner (url ou arquivo local) automaticamente."""
    embed, arquivo = montar_embed(titulo, texto, cor, rodape, banner_url, banner_path)
    kwargs = {"embed": embed}
    if content:
        kwargs["content"] = content
    if arquivo:
        kwargs["file"] = arquivo
    return await destino.send(**kwargs)


def dividir_texto(texto: str, limite: int = 3800) -> list[str]:
    """Divide um texto grande em pedaços que caibam no embed.description.

    Tenta quebrar sempre em uma quebra de linha (\\n) ou espaço pra não
    cortar palavras no meio.
    """
    pedacos = []
    while len(texto) > limite:
        corte = texto.rfind("\n", 0, limite)
        if corte == -1:
            corte = texto.rfind(" ", 0, limite)
        if corte == -1:
            corte = limite
        pedacos.append(texto[:corte].strip())
        texto = texto[corte:].strip()
    if texto:
        pedacos.append(texto)
    return pedacos


async def enviar_texto_grande(
    destino,
    titulo: str,
    texto: str,
    cor: discord.Color = discord.Color.blurple(),
    rodape: str | None = None,
    banner_url: str | None = None,
    banner_path: str | None = None,
    content: str | None = None,
):
    """Divide o texto em vários embeds (até 10) e envia tudo numa mensagem só."""
    pedacos = dividir_texto(texto)
    if not pedacos:
        pedacos = [""]

    if len(pedacos) > 10:
        raise ValueError(
            f"Texto muito grande: gerou {len(pedacos)} embeds, "
            "mas o Discord só permite 10 por mensagem."
        )

    embeds: list[discord.Embed] = []
    for i, pedaco in enumerate(pedacos):
        if i == 0:
            embed = discord.Embed(title=titulo, description=pedaco, color=cor)
            if banner_path:
                nome = os.path.basename(banner_path)
                embed.set_image(url=f"attachment://{nome}")
            elif banner_url:
                embed.set_image(url=banner_url)
        else:
            embed = discord.Embed(
                title=f"{titulo} (continuação {i})",
                description=pedaco,
                color=cor,
            )
        if rodape and i == len(pedacos) - 1:
            embed.set_footer(text=rodape)
        embeds.append(embed)

    kwargs: dict = {"embeds": embeds}
    if content:
        kwargs["content"] = content
    if banner_path:
        nome = os.path.basename(banner_path)
        kwargs["file"] = discord.File(banner_path, filename=nome)

    return await destino.send(**kwargs)