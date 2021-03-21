#coding : utf-8

import logging.config
from multiprocessing import Process

from discord_bot import Dine
from line_bot import Line

def line_run():
    linebot = Line()
    linebot.begin()

def main():
    line_process = Process(target=line_run, daemon=True)
    line_process.start()

    bot = Dine()
    bot.begin()

if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("__name__")

    logging.info("start_program")

    main()