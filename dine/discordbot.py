#coding : utf-8

import os
import discord
from discord.ext import commands

class Dine(commands.Bot):
    def __init__(self):
        super().__init__("!")
    
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Game("dine!"))

    def begin(self):
        self.run(os.environ["DISCORD_TOKEN"])