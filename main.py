import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv(“DISCORD_TOKEN”)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
command_prefix=”!”,
intents=intents
)

——————

JSON 로드

——————

def load_json(path, default):
try:
with open(path, “r”, encoding=“utf-8”) as f:
return json.load(f)
except:
return default

def save_json(path, data):
with open(path, “w”, encoding=“utf-8”) as f:
json.dump(
data,
f,
ensure_ascii=False,
indent=4
)

levels = load_json(“levels.json”, {})
warnings = load_json(“warnings.json”, {})
config = load_json(“config.json”, {})

——————

상태메시지

——————

@bot.event
async def on_ready():

await bot.change_presence(
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="디톤의 노래 실력을 듣고 있는 중 🎵"
    )
)
try:
    synced = await bot.tree.sync()
    print(f"슬래시 명령어 동기화: {len(synced)}개")
except Exception as e:
    print(e)
print(f"로그인 성공: {bot.user}")

——————

레벨 시스템

——————

@bot.event
async def on_message(message):

if message.author.bot:
    return
user_id = str(message.author.id)
if user_id not in levels:
    levels[user_id] = {
        "xp": 0
    }
levels[user_id]["xp"] += 5
save_json("levels.json", levels)
await bot.process_commands(message)

bot.run(TOKEN)
