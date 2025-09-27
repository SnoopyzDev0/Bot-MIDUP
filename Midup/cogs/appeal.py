import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput, Select
from datetime import datetime, timedelta

CANAL_APPEAL_ID = 1416929958382800946
CANAL_ARQUIVO_ID = 1416930113819381791
CARGO_MOD_ID = 1414999281458348054
COOLDOWN_DIAS = 7

appeal_cooldowns = {}

# -------------------- VIEWS --------------------
class AppealView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="🔓 Enviar Appeal", style=discord.ButtonStyle.green, custom_id="enviar_appeal"))

class CasoSelect(Select):
    def __init__(self, user):
        options = [
            discord.SelectOption(label="Ban Permanente", value="Ban Permanente"),
            discord.SelectOption(label="Temp Ban", value="Temp Ban"),
            discord.SelectOption(label="Mute Permanente", value="Mute Permanente"),
            discord.SelectOption(label="Mute Temporario", value="Mute Temporario")
        ]
        super().__init__(placeholder="Selecione seu caso", max_values=1, options=options)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.send_modal(AppealModal(self.user, self.values[0]))

# -------------------- MODAL --------------------
class AppealModal(Modal):
    def __init__(self, user, caso):
        super().__init__(title=f"Revisão de Punição - {caso}")
        self.user = user
        self.caso = caso

        self.nick = TextInput(label="Nick do Usuário", placeholder="Digite seu nick", required=True, max_length=32)
        self.data_punicao = TextInput(label="Data da Punição", placeholder="DD/MM/AAAA", required=True, max_length=20)
        self.motivo = TextInput(label="Motivo para ser desbanido", style=discord.TextStyle.paragraph, required=True)
        self.provas = TextInput(label="Provas (links ou descrição)", style=discord.TextStyle.paragraph, required=False)

        self.add_item(self.nick)
        self.add_item(self.data_punicao)
        self.add_item(self.motivo)
        self.add_item(self.provas)

    async def on_submit(self, interaction: discord.Interaction):
        class ModButtons(View):
            def __init__(self, thread):
                super().__init__(timeout=None)
                self.thread = thread
                self.add_item(Button(label="Aceitar Appeal", style=discord.ButtonStyle.green, custom_id="aceitar_appeal"))
                self.add_item(Button(label="Negar Appeal", style=discord.ButtonStyle.red, custom_id="negar_appeal"))
                self.add_item(Button(label="Excluir Appeal", style=discord.ButtonStyle.grey, custom_id="excluir_appeal"))
                self.add_item(Button(label="Arquivar Appeal", style=discord.ButtonStyle.blurple, custom_id="arquivar_appeal"))

        try:
            embed_logs = discord.Embed(
                title=f"📄 Novo Appeal - {self.caso}",
                description=(
                    f"Usuário: {self.user.mention}\n"
                    f"Nick: {self.nick.value}\n"
                    f"Caso: {self.caso}\n"
                    f"Data da Punição: {self.data_punicao.value}\n"
                    f"Motivo: {self.motivo.value}\n"
                    f"Provas: {self.provas.value if self.provas.value else 'Nenhuma'}"
                ),
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            view = ModButtons(interaction.channel)
            await interaction.channel.send(embed=embed_logs, view=view)
            await interaction.response.send_message("Seu appeal foi registrado na sua thread para revisão da equipe.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro: {e}", ephemeral=True)

# -------------------- COG --------------------
class AppealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def appeal(self, ctx):
        if ctx.author.id in appeal_cooldowns and datetime.utcnow() < appeal_cooldowns[ctx.author.id]:
            await ctx.send(f"Você só pode abrir outro appeal em {appeal_cooldowns[ctx.author.id].strftime('%d/%m/%Y %H:%M UTC')}")
            return
        embed = discord.Embed(
            title="📄 Sistema de Appeals - DripMC",
            description="Clique no botão abaixo para enviar seu appeal. Lembre-se de ser claro e educado ao explicar seu caso.",
            color=discord.Color.orange()
        )
        view = AppealView()
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return

        custom_id = interaction.data.get("custom_id")
        user_id = interaction.user.id

        # ----- BOTÃO ENVIAR APPEAL -----
        if custom_id == "enviar_appeal":
            if user_id in appeal_cooldowns and datetime.utcnow() < appeal_cooldowns[user_id]:
                await interaction.response.send_message(
                    f"Você só pode abrir outro appeal em {appeal_cooldowns[user_id].strftime('%d/%m/%Y %H:%M UTC')}",
                    ephemeral=True
                )
                return

            canal = self.bot.get_channel(CANAL_APPEAL_ID)
            thread = await canal.create_thread(
                name=f"Appeal - {interaction.user.display_name}",
                type=discord.ChannelType.private_thread,
                auto_archive_duration=1440
            )
            await thread.add_user(interaction.user)

            cargo_mod = interaction.guild.get_role(CARGO_MOD_ID)
            if cargo_mod:
                for membro in cargo_mod.members:
                    await thread.add_user(membro)

            view = discord.ui.View()
            view.add_item(CasoSelect(interaction.user))
            embed = discord.Embed(
                title="📌 Appeal",
                description=f"{interaction.user.mention}, selecione seu caso no menu abaixo para iniciar o appeal.",
                color=discord.Color.yellow()
            )
            await thread.send(embed=embed, view=view)
            await interaction.response.send_message("Tópico criado! Você pode escrever seu appeal lá.", ephemeral=True)
            appeal_cooldowns[user_id] = datetime.utcnow() + timedelta(days=COOLDOWN_DIAS)

        # ----- MOD BUTTONS -----
        elif custom_id in ["aceitar_appeal", "negar_appeal", "excluir_appeal", "arquivar_appeal"]:
            cargo_mod = interaction.guild.get_role(CARGO_MOD_ID)
            if not cargo_mod or cargo_mod not in interaction.user.roles:
                await interaction.response.send_message("Você não tem permissão para usar esse botão.", ephemeral=True)
                return

            thread = interaction.channel
            if custom_id == "aceitar_appeal":
                await thread.send("✅ Seu appeal foi **aceito** pela equipe de moderação.")
                await interaction.response.send_message("Appeal aceito.", ephemeral=True)
            elif custom_id == "negar_appeal":
                await thread.send("❌ Seu appeal foi **negado** pela equipe de moderação.")
                await interaction.response.send_message("Appeal negado.", ephemeral=True)
            elif custom_id == "excluir_appeal":
                await interaction.response.send_message("A thread será excluída.", ephemeral=True)
                await thread.delete()
            elif custom_id == "arquivar_appeal":
                canal_arquivo = self.bot.get_channel(CANAL_ARQUIVO_ID)
                embed = discord.Embed(
                    title="📁 Appeal Arquivado",
                    description=f"Thread: {thread.name}\nMotivo: Appeal concluído",
                    color=discord.Color.dark_gray(),
                    timestamp=datetime.utcnow()
                )
                await canal_arquivo.send(embed=embed)
                await interaction.response.send_message("Appeal arquivado com sucesso.", ephemeral=True)
                await thread.edit(archived=True, locked=True)

async def setup(bot):
    await bot.add_cog(AppealCog(bot))