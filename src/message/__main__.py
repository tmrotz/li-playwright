import argparse
from configparser import ConfigParser
from pathlib import Path

from message.streak.Streak import Streak

from . import linkedin, pr

MESSAGE = "message"
SCRAPE = "scrape"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command")
    args = parser.parse_args()
    if args.command is None:
        print("Give one of these commands:", MESSAGE, SCRAPE)
        exit()

    config: ConfigParser = ConfigParser()
    files: list = config.read([
        "config.ini",
        Path.home().joinpath("config.ini").as_posix()
    ])
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

    if args.command == MESSAGE:
        pr.run(config, linkedin.message, streak, config["linkedin"]["message"])
    elif args.command == SCRAPE:
        pr.run(config, linkedin.scrape, streak)
    else:
        print("Invalid command. Use one of these:", MESSAGE, SCRAPE)


if __name__ == "__main__":
    main()
