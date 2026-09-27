from __future__ import annotations

import discord
from discord.ext import commands
from utils.views import enviar_embed


def montar_mensagem_termo() -> str:
    return """## 1 ﹒ REEMBOLSOS

• Cancelamentos antes do início do serviço podem ser aceitos, com desconto de 20% do valor pago referente aos custos operacionais.
• Após o início do serviço, o reembolso será calculado de acordo com o progresso realizado.
• Reembolso integral será realizado somente quando houver impossibilidade da equipe de concluir o serviço.
• Não realizamos reembolso por desistência após a conclusão do serviço.

## 2 ﹒ SEGURANÇA DA CONTA

• O cliente reconhece que determinados serviços podem envolver riscos previstos nos próprios termos e sistemas do jogo.
• A Traveler Store não se responsabiliza por banimentos, suspensões ou punições aplicadas pela desenvolvedora.
• Após a conclusão do pedido, o acesso à conta será encerrado.

## 3 ﹒ PRAZOS E ATENDIMENTO

• O prazo de execução começa a ser contado a partir do momento em que o Farmer recebe acesso à conta.
• A ordem dos pedidos seguirá a fila dos tickets.
• Domingos e feriados não são contabilizados no prazo de execução.
• Nosso suporte funciona 24 horas, porém isso não significa que todos os serviços serão iniciados ou concluídos imediatamente.

## 4 ﹒ CONTAGEM DO SERVIÇO

• Caso o cliente continue acessando a conta durante o serviço, qualquer progresso relacionado ao objetivo contratado poderá ser contabilizado na meta do Farmer.
• O mesmo vale para clientes que decidirem realizar o farm junto com o Farmer.
• Caso existam restrições sobre determinadas missões, eventos ou conteúdos, elas devem ser informadas antes do início do serviço.

## 5 ﹒ COMUNICAÇÃO E CONDUTA

• Todo assunto relacionado aos serviços deve ser tratado exclusivamente pelos tickets oficiais da Traveler Store.
• É proibido realizar negociações ou combinar serviços por mensagens privadas com membros da equipe.
• Respeito é obrigatório durante todo o atendimento.

## 6 ﹒ CONTEÚDO E DIVULGAÇÃO

• A Traveler Store poderá utilizar registros do serviço, como prints ou vídeos de progresso/conclusão, para divulgação da loja.
• A utilização da conta para conteúdos que identifiquem diretamente o cliente poderá ser tratada separadamente com a equipe."""


class Termos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="termos")
    @commands.has_permissions(manage_guild=True)
    async def termos(self, ctx: commands.Context):
        await enviar_embed(
            ctx,
            "୨୧ • Termos de serviço Traveler Store",
            montar_mensagem_termo(),
            discord.Color.blurple(),
            rodape=(
                "A Traveler Store poderá atualizar estes termos sempre que necessário. "
                "A versão válida é a publicada neste canal no momento da contratação. "
                "—— Data 17 de setembro de 2026"
            ),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Termos(bot))