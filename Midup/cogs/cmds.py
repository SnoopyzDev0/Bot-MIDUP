import discord
from discord.ext import commands
from discord import ui

CARGO_PERMITIDO = "Staff ❤️"

class ComandosCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ola(self, ctx):
        await ctx.reply(f"Olá {ctx.author.global_name}. Como posso ajudar?")

    @commands.command()
    async def ping(self, ctx):
        ping_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Ping do bot!",
            description=f"📡 Latência atual: **{ping_ms}ms**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def ip(self, ctx):
        embed = discord.Embed(
            title="🌐 IP DE CONEXÃO",
            description="Conecte-se usando o IP:\ndripmc.com.br",
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def say(self, ctx, *, texto: str = None):
        if not texto:
            await ctx.reply("❌ Você precisa fornecer um texto para o comando.")
            return
        if discord.utils.get(ctx.author.roles, name=CARGO_PERMITIDO):
            await ctx.send(texto)
            print(f"[SAY] {ctx.author.display_name} enviou: {texto}")
        else:
            await ctx.reply("❌ Você não tem permissão para usar este comando.")

    @commands.command()
    async def form(self, ctx):
        embed = discord.Embed(
            title="👮 FORMULÁRIOS",
            description="💘 Se candidate para a nossa equipe:",
            color=discord.Color.blue(),
        )
        embed.add_field(name="👮 Helper", value="[Clique AQUI](https://docs.google.com/forms/d/e/1FAIpQLSfzAcGDrX810aVnjEK_xmB_sSZjVIWj3xDRfvRN_hX8RqwS4g/viewform)", inline=False)
        embed.add_field(name="🎥 Creator", value="[Clique AQUI](https://discord.com/channels/1405235989848391731/1407923405776355378)")
        await ctx.send(embed=embed)


    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="🔎 ATENDIMENTO",
            description="Selecione abaixo a opção que corresponde à sua necessidade:",
            color=discord.Color.blue()
        )
        embed.add_field(name="🔎 Ticket", value="[Clique aqui](https://discord.com/channels/1405235989848391731/1416912904552321074)", inline=False)
        embed.add_field(name="🚨 Denúncias", value="[Clique aqui](https://discord.com/channels/1405235989848391731/1416914821747572758)", inline=False)
        embed.add_field(name="🔓 Appeal", value="[Clique aqui](https://discord.com/channels/1405235989848391731/1416913201836326922)", inline=False)
        embed.set_image(url="https://media.discordapp.net/attachments/1409652423903150131/1414033915147980970/atendimento.png")
        await ctx.send(embed=embed)


    @commands.command()
    async def cmdlist(self, ctx):
        embed = discord.Embed(
            title="📌 LISTA DE COMANDOS",
            description="Todos os comandos disponíveis do bot:",
            color=discord.Color.blue()
        )
        embed.set_footer(text="❓SUPORTE\n!help | !form | !ola | !cmdlist | !loja")
        await ctx.send(embed=embed)

    @commands.command()
    async def loja(self, ctx):
        texto_loja = (
            "**🛒 Loja Oficial DripMC**\n\n"
            "A loja oferece **ranks exclusivos e kits incríveis**, com vantagens únicas "
            "para deixar sua gameplay ainda mais divertida e competitiva!\n\n"
            "**🌐 Acesse agora:** [Clique aqui](https://loja.dripmc.com.br/)"
        )
        embed = discord.Embed(title="🛒 LOJA", description=texto_loja, color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def infoserver(self, ctx: commands.Context, membro: discord.Member = None):
        if membro is None:
            membro = ctx.author
        texto_infoserver = (
            f"**Olá {membro.global_name}, bem-vindo às informações do servidor! "
            "Agradecemos o seu interesse em saber mais sobre o DripMC 🤗**"
        )
        embed = discord.Embed(
            title="📨 Informações do servidor",
            description=texto_infoserver,
            color=discord.Color.green()
        )
        embed.add_field(name="🌐 IP", value="dripmc.com.br", inline=False)
        embed.add_field(name="🛠️ Versão", value="1.8 - 1.21", inline=False)
        embed.add_field(name="🛒 Loja", value="[Clique aqui](https://loja.dripmc.com.br/)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def dev(self, ctx: commands.Context, membro: discord.Member = None):
        if membro is None:
            membro = ctx.author
        texto_infodev = (
            f"**Olá {membro.global_name}, agradecemos o seu interesse em saber mais sobre o nosso desenvolvedor!**\n\n"
            "👨‍💻 O bot foi desenvolvido por **Snoopy** com muito carinho para o servidor DripMC.\n"
            "📌 Caso queira sugerir melhorias ou reportar bugs, utilize os canais de suporte no Discord.\n"
        )
        view = discord.ui.View()
        botao_shop = discord.ui.Button(label="📈 DripStatus", url="https://discord.gg/eRKrJNas")
        view.add_item(botao_shop)
        embed = discord.Embed(
            title="💻 Desenvolvedor do Bot",
            description=texto_infodev,
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=f"{membro.avatar}")
        embed.set_footer(text="DripMC © 2025")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        ping_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Ping do bot!",
            description=f"📡 Latência atual: **{ping_ms}ms**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def regras(self, ctx: commands.Context):
        texto_regras = (
            f"Olá, seja mais que bem-vindo ao Discord Oficial do DripMC. "
            "Estamos ansiosos para ter você interagindo em nosso servidor. "
            "Para isso, leia as regras atentamente e evite ser punido."
        )
        await ctx.send(texto_regras)
        embed = discord.Embed(
            title="📘 Regras do Discord",
            description="Leia com atenção e siga todas as regras para evitar punições.",
            color=discord.Color.blue()
        )
        valorend = (
            "1️⃣ **Retirar** da sua lista de amigos se não quiser mais contato.\n"
            "2️⃣ **Silenciar** o usuário no Discord para não receber mensagens dele.\n"
            "3️⃣ **Bloquear** o jogador caso o comportamento continue.\n"
            "4️⃣ **Chamar a equipe** de moderação utilizando o ticket de denúncia no Discord."
        )
        embed.add_field(name="1. Trate todos com respeito.", value="Todos os membros merecem ser bem tratados.", inline=False)
        embed.add_field(name="2. Assédio ou ofensas não serão tolerados.", value="Mantenha sempre a educação.", inline=False)
        embed.add_field(name="3. Discriminação e discurso de ódio são proibidos.", value="Sem atitudes preconceituosas, beleza?", inline=False)
        embed.add_field(name="4. Evite spam.", value="Não encha o chat com mensagens repetitivas, emojis ou reações excessivas.", inline=False)
        embed.add_field(name="5. Nada de palavrões em excesso.", value="Respeite os filtros de linguagem do servidor.", inline=False)
        embed.add_field(name="6. Não marque Staff ou criadores sem motivo.", value="Eles são ocupados e merecem respeito.", inline=False)
        embed.add_field(name="7. Avatares e status inapropriados não são permitidos.", value="Mantenha seu perfil adequado para todos.", inline=False)
        embed.add_field(name="8. Divulgação de redes sociais ou outros servidores não é aceita.", value="Aqui não é lugar para autopromoção.", inline=False)
        embed.add_field(name="9. Links externos só são permitidos quando relevantes.", value="Use apenas os canais oficiais ou autorizados.", inline=False)
        embed.add_field(name="10. Não compartilhe informações pessoais (suas ou de terceiros).", value="Sua segurança vem em primeiro lugar.", inline=False)
        embed.add_field(name="11. Conteúdos NSFW ou sensuais são proibidos.", value="Queremos um espaço confortável para todos.", inline=False)
        embed.add_field(name="🚨 Caso alguém desrespeite as regras do servidor, você pode:", value=valorend, inline=False)
        await ctx.send(embed=embed)
        embed2 = discord.Embed(
            title="📕 Regras do Servidor",
            description="**Infrações que levam ao banimento:**",
            color=discord.Color.red()
        )
        embed2.add_field(name="Cheating e/ou programas ilegais", value="Uso de hacks ou softwares proibidos.", inline=False)
        embed2.add_field(name="Abuso de bugs", value="Explorar falhas do servidor para se beneficiar.", inline=False)
        embed2.add_field(name="Assédio sexual", value="Qualquer tipo de conteúdo sexual não consentido é inaceitável.", inline=False)
        embed2.add_field(name="Apologia ao nazismo ou similar", value="Conteúdos ofensivos ou de ódio não serão tolerados.", inline=False)
        embed2.add_field(name="Divulgação de servidores", value="Evite promover outros servidores no chat.", inline=False)
        embed2.add_field(name="Forjar provas", value="Mentiras para prejudicar outros jogadores serão punidas.", inline=False)
        embed2.add_field(name="Aliança com cheaters", value="Andar com hackers também é contra as regras.", inline=False)
        embed2.add_field(name="Construções inadequadas", value="Nada de conteúdo ofensivo ou inapropriado.", inline=False)
        embed2.add_field(name="Fraudes eletrônicas", value="Golpes envolvendo dinheiro ou itens são ban permanentes.", inline=False)
        embed2.add_field(name="**Infrações que levam ao mute:**", value=(
            "- Ofensas leves ou piadas de mau gosto\n"
            "- Flood no chat\n"
            "- Discussões desnecessárias\n"
            "- Desrespeito às regras menores"
        ), inline=False)
        await ctx.send(embed=embed2)

    @commands.command()
    async def helper(self, ctx: commands.Context):
        infonessery = (
            "Após o envio do seu formulário, o prazo de validade para uma resposta "
            "para a segunda etapa é de 30 dias. Caso o usuário seja aprovado na aplicação, "
            "será encaminhada uma mensagem ao mesmo, através do Discord. "
            "O usuário que não responder a mensagem da segunda etapa em exatos 7 dias, "
            "será desconsiderado. Não envie mensagens pedindo para o seu formulário ser visto, "
            "isso só diminui suas chances de ser escolhido. "
            "Caso houver identificação de inteligência artificial (como ChatGPT), "
            "o formulário será automaticamente desconsiderado."
        )
        embed = discord.Embed(
            title="👮 Seja helper",
            description=(
                "O servidor está à procura de pessoas que irão se comprometer, "
                "experientes na área, responsáveis, maduros e dispostos a dedicar "
                "um pouco do seu tempo em somar à equipe de moderação."
            ),
            color=discord.Color.blue()
        )
        embed.add_field(
            name="📌 Informações necessárias",
            value=infonessery,
            inline=False
        )
        embed.add_field(
            name="📋 Clique para abrir o formulário abaixo",
            value="[AQUI](https://docs.google.com/forms/d/e/1FAIpQLSfzAcGDrX810aVnjEK_xmB_sSZjVIWj3xDRfvRN_hX8RqwS4g/viewform)",
            inline=False
        )
        embed.set_image(
            url="https://media.discordapp.net/attachments/1326222239540183168/1410001947649507389/formulariohelper.png?ex=68c5d7a4&is=68c48624&hm=25080f50607b0a4cbbb89e9caa5fe05b730395625c1320197e073f21abcf065f&=&format=webp&quality=lossless&width=986&height=257"
        )
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(ComandosCog(bot))