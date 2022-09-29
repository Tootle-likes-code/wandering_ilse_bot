import os

from dotenv import load_dotenv
from wander_bot.bot import WanderingBot


def run():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    default_shut_up_id = int(os.getenv("DEFAULT_SHUT_UP_USER_ID"))

    wandering_bot = WanderingBot(default_shut_up_id=default_shut_up_id)
    wandering_bot.run(token)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
