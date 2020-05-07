import json

import aioredis
import datetime
import discord
from discord.ext import commands

from dungeonkeeper import constants


class Miscellaneous(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Initialise cog attributes."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Listen for new campaign postings, and post an embed in the relevant channel."""
        print("Logged in.")
        self.bot.guild = self.bot.get_guild(constants.Guild.ID)
        self.bot.staging = self.bot.get_guild(constants.Staging.ID)
        self.bot.pool = await aioredis.create_redis_pool("redis://redis")
        self.bot.debug, = await self.bot.pool.psubscribe("campaigns")
        self.bot.listings = self.bot.get_channel(constants.Guild.SESSION_LISTINGS)

        async for channel, message in self.bot.debug.iter():
            campaign = json.loads(message.decode())

            avatar = campaign["avatar"]
            players = campaign["max_players"]
            master_id = campaign["dungeon_master"]
            master = self.bot.get_user(master_id).name

            embed = discord.Embed(
                title=campaign["name"],
                colour=discord.Colour(0xA2812D),
                description=campaign["description"],
            )
            embed.set_author(
                name=f"{master}'s {'campaign' if players < 999 else 'training session'}",
                url=f"https://discordapp.com/users/{master_id}/profile",
                icon_url=f"https://cdn.discordapp.com/avatars/{master_id}/{avatar}.png",
            )
            	
            embed.add_field(name="Date and Time", value=datetime.datetime.fromtimestamp(campaign['datetime']).strftime('%c') + ' UTC', inline=False)
            embed.add_field(name="System", value=campaign["edition"], inline=False)
            embed.add_field(
                name="Player slots",
                value=campaign["max_players"]
                if players != 999
                else "Unlimited (training session)",
                inline=False,
            )
            tags = campaign["tags"]
            for tag in tags:
                emoji = constants.tags[tag]["icon"].replace("-", "")
                emoji = discord.utils.get(self.bot.staging.emojis, name=emoji)
                embed.add_field(name=str(emoji), value=tag)
            if len(tags) % 3 == 2:
                embed.add_field(
                    name="\N{COMBINING GRAPHEME JOINER}",
                    value="\N{COMBINING GRAPHEME JOINER}",
                )
            sessnotify = discord.utils.get(self.bot.guild.roles, name="SessNotify")
            await self.bot.listings.send(sessnotify.mention, embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Miscellaneous(bot))
