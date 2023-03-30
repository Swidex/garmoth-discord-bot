# bot.py
# invite link: https://discord.com/api/oauth2/authorize?client_id=1091099454083436545&permissions=412317240384&scope=bot
# permission code: 412317240384

import discord, os, logging, sys, asyncio
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# DiscordPy Configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@bot.event
async def on_ready():
    logger.info(bot.user.name + " has connected to Discord.")

async def load():
    for fn in os.listdir('./cogs'):
        if fn.endswith('.py'):
            await bot.load_extension(f'cogs.{fn[:-3]}')

async def main():
    await load()
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())