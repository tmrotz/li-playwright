import argparse
import logging
from configparser import ConfigParser
from enum import Enum
from pathlib import Path

from tgl.linkedin.message import Message
from tgl.linkedin.scrape import Scrape
from tgl.playwright import playwright
from tgl.streak.streak import Streak


class Command(Enum):
    MESSAGE = "message"
    SCRAPE = "scrape"
    PIPELINES = "pipelines"

    def __str__(self) -> str:
        return self.value


def main():
    home: Path = Path.home()
    logging.basicConfig(
        filename=home.joinpath("log.log"),
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    )
    logger: logging.Logger = logging.getLogger(__name__)
    logger.debug("hi!")

    config: ConfigParser = ConfigParser()
    files: list = config.read(["config.ini", home.joinpath("config.ini")])
    if len(files) == 0:
        print("Found 0 configs")
        return
    elif len(files) == 1:
        print("Yay! Found a config!")
    elif len(files) > 1:
        print(f"Warning: Found {len(files)} configs")

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
        return

    streak = Streak(config["streak.keys"]["api"])
    streak.pipeline_key = config["streak.keys"]["pipeline"]
    streak.stage_key = config["streak.keys"]["stage"]

    try:
        command: Command = Command(args.command)
    except ValueError:
        print(
            "Invalid command. Use one of these:",
            Command.MESSAGE,
            Command.SCRAPE,
            Command.PIPELINES,
        )
        return

    match command:
        case Command.MESSAGE:
            playwright.run(
                config,
                Message(),
                streak,
                config["linkedin"]["message"],
            )
        case Command.SCRAPE:
            playwright.run(config, Scrape(), streak)
        case Command.PIPELINES:
            print(streak.get_pipelines())


if __name__ == "__main__":
    logger = logging.getLogger("root")
    logger.debug("start")
    try:
        main()
    except Exception as err:
        logger.error(err, exc_info=True)
    logger.debug("stop")
