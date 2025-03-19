import argparse
from configparser import ConfigParser
from pathlib import Path

import pr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="")
    parser.add_argument("-c", "--command")
    args = parser.parse_args()
    if args.command is None:
        print("Give command")
        exit()

    config: ConfigParser = ConfigParser()
    project_dir: Path = Path(__file__).parent.parent
    config.read(project_dir.joinpath("config.ini"))

    pr.run(config, args.command)
