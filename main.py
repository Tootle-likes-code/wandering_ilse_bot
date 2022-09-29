import os

from dotenv import load_dotenv

import bot


def run():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    bot.run_client(token)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
