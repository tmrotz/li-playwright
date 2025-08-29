import argparse
import logging
from configparser import ConfigParser
from enum import Enum
from pathlib import Path

from tgl.linkedin.message import Message
from tgl.linkedin.scrape_network import ScrapeNetwork
from tgl.linkedin.scrape_stage import ScrapeStage
from tgl.linkedin.withdraw import Withdraw
from tgl.playwright import playwright
from tgl.streak.streak import Streak


class Command(Enum):
    MESSAGE = "message"
    SCRAPE = "scrape"
    NETWORK = "network"
    PIPELINES = "pipelines"
    WITHDRAW = "withdraw"

    def __str__(self) -> str:
        return self.value


def main():
    config: ConfigParser = ConfigParser()
    files: list = config.read(["config.ini", Path.home().joinpath("config.ini")])
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
            [c.value for c in Command],
        )
        return

    streak = Streak(config["streak.keys"]["api"], config["streak.keys"]["pipeline"])

    try:
        command: Command = Command(args.command)
    except ValueError:
        print(
            "Invalid command. Use one of these:",
            [c.value for c in Command],
        )
        return None

    match command:
        case Command.MESSAGE:
            playwright.run(
                config,
                Message(),
                streak,
                config["linkedin"]["message"],
                config["stages"]["message"],
                config["stages"]["messaged"],
            )
        case Command.SCRAPE:
            playwright.run(
                config,
                ScrapeStage(),
                streak,
                config["stages"]["scrape"],
                config["stages"]["scraped"],
            )
        case Command.NETWORK:
            playwright.run(config, ScrapeNetwork(), streak)
        case Command.PIPELINES:
            print(streak.get_pipelines())
        case Command.WITHDRAW:
            playwright.run(config, Withdraw())


if __name__ == "__main__":
    logging.basicConfig(
        filename=Path.home().joinpath("log.log"),
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    )
    logger: logging.Logger = logging.getLogger()
    logger.debug("start")

    try:
        main()
    except Exception as err:
        print("Something went wrong. Check ~/log.log", err)
        logger.error(err, exc_info=True)

    logger.debug("stop")
