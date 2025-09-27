import asyncio
import discord
from discord.ext import commands, tasks
from discord.ext import commands
from mcstatus import JavaServer
import json
import os
from datetime import datetime, timedelta



server = JavaServer("131.196.198.49")
status_channel_id = 1421252608940576798
status_message_id = None
CONFIG_FILE = "config_status.json"
IP_VISUAL = "midup.com.br"
VERSAO_VISUAL = "1.8 - 1.21"
CARGO_PERMITIDO = 1421253388602970153
WEBHOOK_URL = "https://discord.com/api/webhooks/1421253281728167997/f3VtNiC7hMI95B6WkjL5pIigmsTOdJKyTWIjPf_I1UII6PHuVZ9p4QiSsJ-cFPcp2lYk"
CANAL_PLAYER_COUNT = 1421252571120799855


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
status_message = None


def salvar_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump({"status_message_id": status_message_id}, f)

def carregar_config():
    global status_message_id
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            status_message_id = data.get("status_message_id")
            print(f"[INFO] ID da mensagem carregado: {status_message_id}")


@tasks.loop(minutes=2)
async def update_status():
    global status_message
    try:
        status = await asyncio.to_thread(server.status)
        online = True
        player_count = status.players.online
        max_players = status.players.max
    except Exception as e:
        print(f"[ERRO STATUS] {e}")
        online = False
        player_count = 0
        max_players = "???"

    canal_status = bot.get_channel(status_channel_id)
    canal_nome = bot.get_channel(CANAL_PLAYER_COUNT)
    if not canal_status:
        print("[ERRO] Canal de status não encontrado.")
        return

    if not status_message and status_message_id:
        try:
            status_message = await canal_status.fetch_message(status_message_id)
            print(f"[INFO] Mensagem de status carregada com sucesso.")
        except discord.NotFound:
            print(f"[ERRO] A mensagem de status foi deletada. Rode !setupstatus novamente.")
            return
        except Exception as e:
            print(f"[ERRO AO BUSCAR MENSAGEM PELO ID] {e}")
            return

    if not status_message:
        print("[ERRO] Nenhuma mensagem de status disponível. Rode !setupstatus.")
        return

    embed = discord.Embed(
        title="🟢 Servidor Online" if online else "🔴 Servidor Offline",
        color=discord.Color.green() if online else discord.Color.red()
    )
    embed.add_field(name="👥 Jogadores Online", value=f"{player_count}/{max_players}", inline=False)
    embed.add_field(name="🌐 IP do Servidor", value=f"{IP_VISUAL}", inline=False)
    embed.add_field(name="🛠️ Versão", value=VERSAO_VISUAL, inline=False)
    embed.add_field(name="📡 Status", value="Online" if online else "Offline", inline=False)
    embed.set_footer(text=f"Atualizado em {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S UTC')}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1415011214217488394/1416886799004561498/k.png")

    try:
        await status_message.edit(embed=embed)
        print("[INFO] Mensagem de status atualizada.")
    except discord.NotFound:
        print("[ERRO] A mensagem de status foi deletada. Rode !setupstatus novamente.")
        return
    except Exception as e:
        print(f"[ERRO AO EDITAR EMBED] {e}")

    if canal_nome:
        canal_name = "🔴 Offline" if not online else f"🎮 Jogadores: {player_count}"
        if canal_nome.name != canal_name:
            try:
                await canal_nome.edit(name=canal_name)
                print("[INFO] Nome do canal atualizado.")
            except Exception as e:
                print(f"[ERRO AO EDITAR CANAL] {e}")

    status_text = "💻 Servidor OFFLINE" if not online else f"🎮 {player_count} players online"
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(status_text))


@bot.event
async def on_ready():
    print("Bot online")
    carregar_config()
    cogs = ["cogs.cmds", "cogs.appeal", "cogs.eventos", "cogs.tickets", "cogs.responses"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"[INFO] Cog {cog} carregada.")
        except Exception as e:
            print(f"[ERRO] Não foi possível carregar {cog}: {e}")
    if status_message_id:
        update_status.start()
    else:
        print("[INFO] Nenhum status_message_id encontrado, rode !setupstatus para criar a mensagem.")

@bot.command()
async def setupstatus(ctx):
    global status_message, status_message_id
    embed = discord.Embed(
        title="🟢 Servidor Online",
        color=discord.Color.green()
    )
    embed.add_field(name="👥 Jogadores Online", value="Buscando...", inline=False)
    embed.add_field(name="🌐 IP do Servidor", value=f"{IP_VISUAL}", inline=False)
    embed.add_field(name="🛠️ Versão", value=VERSAO_VISUAL, inline=False)
    embed.add_field(name="📡 Status", value="Buscando...", inline=False)
    embed.set_footer(text="Atualizado a cada 2 minutos - Aguardando primeira atualização")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1415011214217488394/1416886799004561498/k.png")
    view = discord.ui.View()
    botao_shop = discord.ui.Button(label="🛒 Loja", url="https://loja.dripmc.com.br/")
    botao_yt = discord.ui.Button(label="🎥Youtube",url="https://www.youtube.com/@dripmcbr")
    botao_ttk = discord.ui.Button(label="🎵Tik Tok", url="https://www.tiktok.com/@dripmcbr/")
    view.add_item(botao_shop)
    view.add_item(botao_yt)
    view.add_item(botao_ttk)
    msg = await ctx.send(embed=embed, view=view)
    status_message = msg
    status_message_id = msg.id
    salvar_config()
    await ctx.send("✅ Mensagem de status criada e salva com sucesso!")
    if not update_status.is_running():
        update_status.start()







bot.run("MTQyMTI1NDExNzQ4MDg2MTc2Nw.Gdm6bM.8raZiPL9WqlyGoyxyIGu1_IwroC9ucGUGj8oWM")