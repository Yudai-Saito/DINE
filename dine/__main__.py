#coding : utf-8

import logging.config
from multiprocessing import Process

from discord_bot import Dine
from line_bot import Line
from db import create_db

def line_run():
    linebot = Line()
    linebot.begin()

def discord_run():
    bot = Dine()
    bot.begin()

def main():
    line_process = Process(target=line_run, daemon=True)
    line_process.start()

    discord_process = Process(target=discord_run, daemon=True)
    discord_process.start()

    while True:
        #time schedule
        pass

if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("__name__")

    logging.info("start_program")

    create_db()

    main()