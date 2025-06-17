import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re  # para regex

load_dotenv()

TOKEN = os.getenv("")
CANAL_PUBLICO_ID = 1383839696659943464  # seu canal público
CANAL_LOGS_ID = 1383839669023932459    # seu canal privado

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot logado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == CANAL_PUBLICO_ID:
        canal_logs = bot.get_channel(CANAL_LOGS_ID)

        # Tenta extrair a quantidade da mensagem (primeiro número inteiro)
        match = re.search(r'\b(\d+)\b', message.content)
        quantidade = match.group(1) if match else "Quantidade não informada"

        embed = discord.Embed(
            title="📥 Nova entrega de farm registrada",
            description=message.content or "*Mensagem sem texto*",
            color=discord.Color.green(),
            timestamp=message.created_at
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url if message.author.avatar else None)
        embed.add_field(name="👤 Usuário", value=message.author.mention, inline=True)
        embed.add_field(name="📦 Quantidade", value=quantidade, inline=True)
        embed.add_field(name="🕒 Data e Hora", value=message.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        
        if message.attachments:
            anexos = "\n".join([att.url for att in message.attachments])
            embed.add_field(name="📎 Anexos", value=anexos, inline=False)

        await canal_logs.send(embed=embed)
        await message.delete()

    await bot.process_commands(message)
    
from keep_alive import keep_alive  # importa o servidor

keep_alive()  # ativa o servidor web

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot ativo!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

bot.run("")
