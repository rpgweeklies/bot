import discord
from discord.ext import commands

from dungeonkeeper.queries import get_field, set_field, user_exists


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Initialise cog attributes."""
        self.bot = bot

    @commands.has_any_role('Director', 'Puppet Masters')
    @commands.command()
    async def modify(
        self, ctx: commands.Context, user: discord.Member, target: str, difference: int
    ) -> None:
        """
        Modify a user's experience or gold amount.

        >modify tablesalt gold -100
        >modify Aperture exp +20
        """
        db_map = {"exp":"experience","gold":"gold"}
        if target in db_map.keys():
            value = await get_field(db_map[target], user.id)
            if value is None:
                await ctx.send(f"{user.mention} hasn't signed in yet! They can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
            else:
                value += difference
                await set_field(db_map[target], user.id, value)
                if difference >= 0:
                    message = 'Added {change} {category} to {user}. '
                else:
                    message = 'Removed {change} {category} from {user}. '
                message += 'They now have {total} {category}!'
                await ctx.send(message.format(
                        total=value,
                        category=db_map[target],
                        user=user.mention,
                        change=abs(difference)
                    ))
        else:
            await ctx.send('Invalid field. Please use `exp` or `gold`.')
            
    @commands.has_any_role('Director', 'Puppet Masters')
    @commands.command()
    async def rewardbump(self, ctx: commands.Context, user: discord.Member, quan: int = 1) -> None:
        """Reward a player with 10*n gold for bumping the server.
        
        >rewardbump tablesalt
        >rewardbump tablesalt 2
        """
        value = await get_field("gold", user.id)
        if value is None:
            await ctx.send(f"{user.mention} hasn't signed in yet! They can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
        else:
            value += (10 * quan)
            await set_field("gold", user.id, value)
            message = f'Given {10*quan} gold to {user.mention}. Thanks for bumping!'
            await ctx.send(message)

    @commands.has_any_role('Director', 'Puppet Masters')
    @commands.command()
    async def set(
        self, ctx: commands.Context, user: discord.Member, target: str, value: int
    ) -> None:
        """
        Set a user's experience or gold amount.

        >set tablesalt gold 0
        >set Aperture exp 30
        """
        db_map = {"exp":"experience","gold":"gold"}
        if target in db_map.keys():
            if not await user_exists(user.id):
                await ctx.send(f"{user.mention} hasn't signed in yet! They can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
            else:
                await set_field(db_map[target], user.id, value)
                await ctx.send(
                    f"Set {user.mention}'s {db_map[target]} to {value}!"
                    )
        else:
            await ctx.send('Invalid field. Please use `exp` or `gold`.')
                
    @commands.has_any_role('Director', 'Puppet Masters')
    @commands.command()
    async def toggldm(self, ctx: commands.Context, user: discord.Member) -> None:
        """Toggle someone having the DungeonMaster role.
        
        >toggledm tablesalt"""
        # TODO: Maybe make this influence the site too, and vice versa
        sessnotify = await commands.RoleConverter().convert(ctx, "DM")
        roles = user.roles
        if sessnotify in roles:
            roles.remove(sessnotify)
            await user.edit(roles=roles)
            await ctx.send(f"{user.mention} is no longer a DM.")
        else:
            roles.append(sessnotify)
            await user.edit(roles=roles)
            await ctx.send(f"{user.mention} is now a DM.")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Admin(bot))
