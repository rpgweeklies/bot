import discord, random
from discord.ext import commands

from dungeonkeeper.queries import get_field

class Player(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Initialise cog attributes."""
        self.bot = bot

    @commands.command()
    async def gold(self, ctx: commands.Context, player: discord.Member = None) -> None:
        """Retrieve the gold amount of a player.
        
        >gold tablesalt
        >gold
        """
        player = player or ctx.author
        gold = await get_field("gold", player.id)
        if gold is None and player is not ctx.author:
            await ctx.send(f"{player.mention} hasn't signed in yet! They can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
        elif gold is None and player is ctx.author:
            await ctx.send(f"You haven't signed in yet! You can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
        elif player is ctx.author:
            await ctx.send(f"{player.mention}, you have {gold} gold!")
        else:
            await ctx.send(f"{player.mention} has {gold} gold!")
            
            
    @commands.command()
    async def rolldice(self, ctx: commands.Context, num: int = 1, sides: int = 20) -> None:
        """Roll a number of dice with various sides
        
        >rolldice
        >rolldice 2 20
        >rolldice 1
        """
        # num = 4 https://xkcd.com/221/
        rolls = [random.randint(1, sides) for roll in "a"*num]
        await ctx.send(f"Rolled {', '.join(map(str,rolls))}.{f' (Total: {sum(rolls)})' if num >= 5 else ''}")
        

    @commands.command()
    async def exp(self, ctx: commands.Context, player: discord.Member = None) -> None:
        """Retrieve the experience of a player.
        
        >exp tablesalt
        >exp
        """
        player = player or ctx.author
        experience = await get_field("experience", player.id)
        if experience is None and player is not ctx.author:
            await ctx.send(f"{player.mention} hasn't signed in yet! They can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
        if experience is None and player is ctx.author:
            await ctx.send(f"You haven't signed in yet! You can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
        elif player is ctx.author:
            await ctx.send(f"{player.mention}, you have {experience} experience!")
        else:
            await ctx.send(f"{player.mention} has {experience} experience!")
    
    @commands.command()
    async def togglenotify(self, ctx: commands.Context) -> None:
        """Toggle having the SessNotify role.
        
        >togglenotify"""
        player = ctx.author
        sessnotify = await commands.RoleConverter().convert(ctx, "SessNotify")
        roles = player.roles
        if sessnotify in roles:
            roles.remove(sessnotify)
            await player.edit(roles=roles)
            await ctx.send(f"{player.mention}, you no longer have the SessNotify role.")
        else:
            roles.append(sessnotify)
            await player.edit(roles=roles)
            await ctx.send(f"{player.mention}, you now have the SessNotify role.")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Player(bot))
