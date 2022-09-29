from discord.ext import commands


class DiceRollerCog(commands.Cog):
    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, die_function: str):
        print(die_function)