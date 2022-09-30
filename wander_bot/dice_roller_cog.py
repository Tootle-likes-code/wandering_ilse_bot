from discord.ext import commands
from discord.ext.commands import BadArgument, MissingRequiredArgument


class DiceRollerCog(commands.Cog):
    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, die_function: str):
        print(die_function)

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("You need to give a dice string.  Come on.")
