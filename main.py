import os

from dotenv import load_dotenv
from bot import WanderingBot


def run():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    wandering_bot = WanderingBot()
    wandering_bot.run(token)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
