import argparse
from configparser import ConfigParser
from enum import Enum
from pathlib import Path

from tgl.linkedin.message import send_messages
from tgl.linkedin.scrape import scrape
from tgl.playwright import playwright
from tgl.streak.streak import Streak


class Command(Enum):
    MESSAGE = "message"
    SCRAPE = "scrape"
    PIPELINES = "pipelines"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command")
    args = parser.parse_args()
    if args.command is None:
        print(
            "Give one of these commands:",
            Command.MESSAGE,
            Command.SCRAPE,
            Command.PIPELINES,
        )
        exit()

    config: ConfigParser = ConfigParser()
    files: list = config.read(
        ["config.ini", Path.home().joinpath("config.ini").as_posix()]
    )
    if len(files) == 0:
        print("Found 0 configs")
        quit()
    elif len(files) == 1:
        print("Yay! Found a config!")
    elif len(files) > 1:
        print(f"Warning: Found {len(files)} configs")

    streak = Streak(config["streak.keys"]["api"])
    streak.pipeline_key = config["streak.keys"]["pipeline"]
    streak.stage_key = config["streak.keys"]["stage"]

    match args.command:
        case Command.MESSAGE:
            playwright.run(
                config,
                send_messages,
                streak,
                config["linkedin"]["message"],
            )
        case Command.SCRAPE:
            playwright.run(config, scrape, streak)
        case Command.PIPELINES:
            print(streak.get_pipelines())
        case _:
            print(
                "Invalid command. Use one of these:",
                Command.MESSAGE,
                Command.SCRAPE,
                Command.PIPELINES,
            )


if __name__ == "__main__":
    main()
