from discord.ext import commands
from discord.ext.commands import BadArgument


class DiceRollerCog(commands.Cog):
    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, die_function: str):
        print(die_function)

    @roll.error()
    async def roll(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send(f"You need to give a valid dice string.  Come on.")