"""Interact with the config file."""
import configparser
import os
from pathlib import Path

DEFAULT = "DEFAULT"
HOME_PATH = str(Path.home())
CENSYS_PATH = os.path.join(HOME_PATH, ".config", "censys")
CONFIG_PATH = os.path.join(CENSYS_PATH, "censys.cfg")

default_config = {
    "api_id": "",
    "api_secret": "",
    "asm_api_key": "",
    "color": "auto",
}


def get_config_path() -> str:
    """Returns the path to the config file.

    Returns:
        str: Path to config file.
    """
    alt_path = os.getenv("CENSYS_CONFIG_PATH")
    if alt_path:
        return alt_path
    return CONFIG_PATH


def write_config(config: configparser.ConfigParser) -> None:
    """Writes config to file.

    Args:
        config (configparser.ConfigParser): Configuration to write.

    Raises:
        PermissionError: If the config file is not writable.
    """
    config_path = get_config_path()
    if config_path == CONFIG_PATH:
        if not os.access(HOME_PATH, os.W_OK):
            raise PermissionError(
                "Cannot write to home directory. Please set the `CENSYS_CONFIG_PATH` environmental variable to a writeable location."
            )
        elif not os.path.isdir(CENSYS_PATH):
            os.makedirs(CENSYS_PATH)
    with open(config_path, "w") as configfile:
        config.write(configfile)


def get_config() -> configparser.ConfigParser:
    """Reads and returns config.

    Returns:
        configparser.ConfigParser: Config for Censys.
    """
    config = configparser.ConfigParser(defaults=default_config, default_section=DEFAULT)
    config_path = get_config_path()
    if os.path.isfile(config_path):
        config.read(config_path)
    return config
