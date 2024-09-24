import discord
from discord.ext import commands
from requests_oauthlib import OAuth2Session
import os
from aiohttp import web
import asyncio

intents = discord.Intents.default() 
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="b.", intents=intents)

CLIENT_ID = os.getenv('ION_CLIENT_ID')
CLIENT_SECRET = os.getenv('ION_CLIENT_SECRET')
REDIRECT_URI = os.getenv('ION_REDIRECT_URI')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
SENIOR_ROLE_ID = os.getenv('SENIOR_ROLE_ID')
AUTHORIZATION_URL = "https://ion.tjhsst.edu/oauth/authorize/"
TOKEN_URL = "https://ion.tjhsst.edu/oauth/token/"
PROFILE_URL = "https://ion.tjhsst.edu/api/profile/"

def create_oauth_session():
    return OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["read"])

oauth_state = {}

@bot.command(name="verify")
async def verify(ctx):
    oauth = create_oauth_session()
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_URL)

    oauth_state[state] = {
        'discord_user_id': ctx.author.id,
        'channel_id': ctx.channel.id
    }

    #send link
    await ctx.send(f"Please follow the link in your Direct Messages to continue verification.")
    await ctx.author.send(f"Click here to verify: {authorization_url}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {repr(message.content)}")
    await bot.process_commands(message)


@bot.command(name="wadu")
async def ping(ctx):
    await ctx.send("hek!")

@bot.command(name="info")
async def help(ctx):
    await ctx.send("Usage: b.verify.")

async def handle_callback(request):
    code = request.query.get('code')
    state = request.query.get('state')

    if state not in oauth_state:
        return web.Response(text="Invalid OAuth state.")

    oauth = create_oauth_session()
    token = oauth.fetch_token(TOKEN_URL, code=code, client_secret=CLIENT_SECRET)

    profile = oauth.get(PROFILE_URL).json()
    discord_user_id = oauth_state[state]['discord_user_id']
    channel_id = oauth_state[state]['channel_id']

    if profile.get('graduation_year') == 2025:
        guild = bot.get_guild(int(GUILD_ID))
        role = guild.get_role(int(SENIOR_ROLE_ID))
        member = guild.get_member(discord_user_id)

        if role not in member.roles:
            await member.add_roles(role)

            channel = bot.get_channel(channel_id)
            await channel.send(f"<@{discord_user_id}> has been verified and assigned the verified role.")
        else:
            channel = bot.get_channel(channel_id)
            await channel.send(f"<@{discord_user_id}> already has the verified role.")
    else:
        channel = bot.get_channel(channel_id)
        await channel.send(f"<@{discord_user_id}> is not in the senior class. If you are in ScavComm, please ping an admin with proof.")

    del oauth_state[state]

    return web.Response(text="Verification complete. You can return to Discord now.")

app = web.Application()
app.router.add_get("/callback", handle_callback)

async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 5000) 
    await site.start()

    local_url = f"{os.getenv('ION_REDIRECT_URI')}"
    print(f"Local server is running at: {local_url}")

    # start the bot
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

#Brian Ho, TJHSST Class of 2025
