import discord
from discord.ext import commands

from dungeonkeeper.constants import rewards
from dungeonkeeper.queries import get_field, set_field, user_exists


class DungeonMaster(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Initialise cog attributes."""
        self.bot = bot

    @commands.has_role('DM')
    @commands.command()
    async def reward(
        self, ctx: commands.Context, user: discord.Member, reward_class: str
    ) -> None:
        """
        Reward a player with gold and experience.

        reward_class must be one of: player, ondeck, spectator.
        """
        if reward_class not in ('player', 'ondeck', 'spectator'):
            return await ctx.send("Reward class must be one of: player, ondeck, spectator")
        if not await user_exists(user.id):
            return await ctx.send(f"{user.mention} hasn't signed in yet! They can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
        gold = await get_field("gold", user.id)
        exp = await get_field("experience", user.id)
        if gold is None or exp is None:
            return await ctx.send(f"{user.mention} hasn't signed in yet! They can sign in at https://rpgweeklies.ml/ to start earning gold & experience.")
        gold_reward, exp_reward = rewards.get(reward_class.lower())
        gold += gold_reward
        exp += exp_reward
        await set_field("gold", user.id, gold)
        await set_field("experience", user.id, exp)
        if reward_class == "spectator":
            await ctx.send(
                f"{user.mention} has been rewarded with {gold_reward} gold. "
                f"They now have {gold} gold!"
            )
        else:
            await ctx.send(
                f"{user.mention} has been rewarded with {gold_reward} gold, "
                f"{exp_reward} experience. They now have {gold} gold, and {exp} experience!"
            )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(DungeonMaster(bot))
