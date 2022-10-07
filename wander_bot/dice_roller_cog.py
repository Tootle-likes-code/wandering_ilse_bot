import pydice.dice_string_interpreter
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, Context
from pydice.roll_result import RollResult


class DiceRollerCog(commands.Cog):
    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx: Context, dice_string: str):
        result: RollResult = pydice.dice_string_interpreter.interpret(dice_string)

        if result is None:
            await ctx.send(f"<@{ctx.author.id}>, your dice string doesn't work.  You should check out: " 
                           f"https://github.com/Tootle-likes-code/pydice/blob/main/README.md")
        else:
            message = f"<@{ctx.author.id}> rolled {dice_string}.\n" \
                      f"`Dice Roll: {result.die_rolls}`\n" \
                      f"Result: {result.result()}"

            await ctx.send(message)

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("You need to give a dice string.  Come on.")
