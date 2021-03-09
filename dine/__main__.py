#coding : utf-8

import logging.config
from discordbot import Dine

def main():
    bot = Dine()
    bot.begin()

if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("__name__")

    logging.info("start_program")

    main()