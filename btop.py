#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


light_theme = "flat-remix-light"
dark_theme = "onedark"


# "default" or "prefer-dark"
def get_color_scheme():
    result = subprocess.run(
        ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().strip("'")


def update_config():
    mode = "dark" if get_color_scheme() == "prefer-dark" else "light"

    color_theme = dark_theme if mode == "dark" else light_theme

    # Path to btop's config file in the user's home
    config = (
        Path(os.path.expanduser("~"))
        .joinpath(".config")
        .joinpath("btop")
        .joinpath("btop.conf")
    )

    # Read the config, replacing the `color_theme` statement based on the `mode`
    lines = []

    with config.open() as file:
        for line in file:
            if line.startswith("color_theme"):
                current_theme = line.split("=")[1].strip().strip('"')
                if current_theme == color_theme:
                    # Theme is already set to the desired one
                    return
            lines.append(line)

    new_lines = [
        (
            line
            if not line.startswith("color_theme")
            else f'color_theme = "{color_theme}"\n'
        )
        for line in lines
    ]

    # Write the new config
    with config.open("w") as file:
        for line in new_lines:
            file.write(line)


def main():
    update_config()

    # Launch btop
    # subprocess.run(["/usr/bin/btop"] + sys.argv[1:], check=False)


if __name__ == "__main__":
    main()
