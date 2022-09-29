import discord
from discord import client

intents = discord.Intents.default()
intents.message_content = True

client = discord.client.Client(intents=intents)


def run_client(token: str):
    client.run(token)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!!")
