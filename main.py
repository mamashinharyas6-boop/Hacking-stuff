import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class HIFramework(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix='h!', #h! h is name for hack
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Load all cogs from /cogs folder
        if os.path.exists("./cogs"):
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"🔥 Loaded Module: {filename}")

    async def on_ready(self):
        # Force DND status
        await self.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name="Hacking 🔥")
        )

        print("====================================")
        print(f"🚀 Logged in as: {self.user}")
        print("🔴 Status: Do Not Disturb")
        print("====================================")

# Create bot instance
bot = HIFramework()

# Run bot (NO status here)
bot.run(os.getenv("DISCORD_TOKEN"))
