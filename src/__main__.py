import argparse
from configparser import ConfigParser
from pathlib import Path

import linkedin
import pr
from streak.Streak import Streak

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="")
    parser.add_argument("-c", "--command")
    args = parser.parse_args()
    if args.command is None:
        print("Give one of these commands:", "message", "scrape")
        exit()

    config: ConfigParser = ConfigParser()
    project_dir: Path = Path(__file__).parent.parent
    config.read(project_dir.joinpath("config.ini"))

    streak = Streak(config["streak.keys"]["api"])
    streak.pipeline_key = config["streak.keys"]["pipeline"]
    streak.stage_key = config["streak.keys"]["stage"]

    if args.command == "message":
        pr.run(config, linkedin.message, streak, config["linkedin"]["message"])
    elif args.command == "scrape":
        pr.run(config, linkedin.scrape, streak)
    else:
        print("Invalid command. Use one of these:", "message", "scrape")
