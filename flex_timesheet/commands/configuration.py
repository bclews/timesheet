import json
import os
from pathlib import Path

import typer

import flex_timesheet.common.configuration as conf


def configure(config_path: Path):
    if config_path is None:
        config_path = conf.get_default_config_path()

    config_data = conf.read(config_path)

    config_data["timesheet_file"] = os.path.expanduser(
        typer.prompt(
            "Enter the location to save your timesheet",
            default=config_data.get("timesheet_file", "~/timesheet.json"),
        )
    )

    conf.write(config_path, config_data)
    typer.echo(f"Configuration saved to {config_path}")


def show_config(config_path: Path):
    if config_path is None:
        config_path = conf.get_default_config_path()

    config_data = conf.read(config_path)
    typer.echo(json.dumps(config_data, indent=4))
