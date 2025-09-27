import discord
from discord.ext import commands
import traceback
import aiohttp

WEBHOOK_URL = "https://discord.com/api/webhooks/1415051800884809848/b5C0n_UCMLpehAha7RZf2R8avImmL3Iu3oeSoey-VidwJ1-IhfsBpwNK3mfO19z49cl1"

class EventosCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def enviar_erro_webhook(self, erro_msg):
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)
            await webhook.send(content=f"**Erro no Bot:**\n```py\n{erro_msg}\n```")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot online")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        erro_formatado = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        await self.enviar_erro_webhook(erro_formatado)
        await ctx.send("❌ Ocorreu um erro! Ele foi reportado aos administradores.")

    @commands.Cog.listener()
    async def on_error(self, event_method, *args, **kwargs):
        erro_formatado = traceback.format_exc()
        await self.enviar_erro_webhook(erro_formatado)
        raise

    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        canal_logs = self.bot.get_channel(1415000284513566864)
        if canal_logs:
            await canal_logs.send(
                f"🗑️ Mensagem deletada no canal {msg.channel.mention}\n"
                f"👤 Autor: {msg.author.mention}\n"
                f"💬 Conteúdo: {msg.content if msg.content else '[Mensagem vazia/embeds]'}"
            )

    @commands.Cog.listener()
    async def on_member_join(self, membro: discord.Member):
        canal = self.bot.get_channel(1415002124139630682)
        if canal:
            await canal.send(
                f"📂 Um usuário entrou no servidor!\n"
                f"👤 Nome: {membro.mention}\n"
                f"🆔 ID: **{membro.id}**"
            )

    @commands.Cog.listener()
    async def on_member_remove(self, membro: discord.Member):
        canal = self.bot.get_channel(1415015677034631239)
        if canal:
            await canal.send(
                f"📨 Um usuário saiu do servidor!\n"
                f"👤 Nome: {membro.mention}\n"
                f"🆔 ID: **{membro.id}**"
            )

async def setup(bot):
    await bot.add_cog(EventosCog(bot))