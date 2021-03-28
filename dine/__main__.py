#coding : utf-8

import schedule
import logging.config
from multiprocessing import Process

from discord_bot import Dine
from line_bot import Line
from db import create_db, ScheduleManager

def line_run():
    linebot = Line()
    linebot.begin()

def discord_run():
    bot = Dine()
    bot.begin()

def user_delete():
    db_schedule = ScheduleManager()
    db_schedule.time_over_user()

def schedule_function():
    schedule.every(1).minutes.do(user_delete)

    while True:
        schedule.run_pending()

def main():
    line_process = Process(target=line_run, daemon=True)
    line_process.start()

    discord_process = Process(target=discord_run, daemon=True)
    discord_process.start()

    schedule_function()

if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("__name__")

    logging.info("start_program")

    create_db()

    main()