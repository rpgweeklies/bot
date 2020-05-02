import discord
from discord.ext import commands

from dungeonkeeper.queries import get_field, set_field, user_exists
from dungeonkeeper.constants import roleshop

class Shop(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Initialise cog attributes."""
        self.bot = bot

    @commands.command()
    async def buyrole(self, ctx: commands.Context, *rolename: str) -> None:
        """Buy a role from the shop!
        
        >buyrole <rolename>"""
        if any(type(i) != str for i in rolename):
            await ctx.send("Why did you even try that?")
            return
        rolename = " ".join(rolename).lower()
        try:
            goldcost, expreq = roleshop[rolename]
        except KeyError:
            await ctx.send("That role doesn't exist!")
            return
        user = ctx.author
        usergold = await get_field("gold", user.id)
        userexp = await get_field("experience", user.id)
        if usergold == None or userexp == None:
            await ctx.send("You haven't logged in yet!")
            return
        if userexp < expreq:
            await ctx.send("You don't have enough experience to buy this role!")
            return
        if usergold < goldcost:
            await ctx.send("You don't have enough gold to buy this role!")
            return
        roles = ctx.guild.roles
        roletable = {}
        for role in roles:
            roletable[role.name.lower()] = role.id
        if rolename not in roletable.keys():
            await ctx.send("This role doesn't exist on the server!")
            return
        new_role = await commands.RoleConverter().convert(ctx, str(roletable[rolename]))
        if new_role in user.roles:
            await ctx.send("You already have that role!")
            return
        new_roles = user.roles
        new_roles.append(new_role)
        await user.edit(roles=new_roles)
        await ctx.send(f"{user.mention}, you have bought the `{new_role.name}` role!")
        await set_field("gold", user.id, usergold - goldcost)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Shop(bot))
