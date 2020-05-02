from discord import Game
from discord.ext import commands


bot = commands.Bot(command_prefix=">", activity=Game(name=">help"))

bot.load_extension("dungeonkeeper.cogs.dm")
bot.load_extension("dungeonkeeper.cogs.misc")
bot.load_extension("dungeonkeeper.cogs.admin")
bot.load_extension("dungeonkeeper.cogs.player")
bot.load_extension("dungeonkeeper.cogs.shop")
