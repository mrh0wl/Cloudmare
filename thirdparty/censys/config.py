"""
Interact with the config file.
"""

import os
from pathlib import Path
from configparser import ConfigParser, NoOptionError

from thirdparty.censys import __version__

DEFAULT = "DEFAULT"

xdg_config_path = os.path.join(str(Path.home()), ".config")
censys_path = os.path.join(xdg_config_path, "censys")
config_path = os.path.join(censys_path, "censys.cfg")

default_config = {
    "version": __version__,
    "api_id": "",
    "api_secret": "",
}


def write_config(config):
    """
    Writes config to file.

    Args:
        config: Configuration to write.
    """

    with open(config_path, "w") as configfile:
        config.write(configfile)


def get_config():
    """
    Reads and returns config.
    """

    config = ConfigParser()
    if not os.path.isdir(xdg_config_path):
        os.mkdir(xdg_config_path)
    if not os.path.isdir(censys_path):
        os.mkdir(censys_path)
    if not os.path.exists(config_path):
        config[DEFAULT] = default_config
        with open(config_path, "w") as configfile:
            config.write(configfile)
    config.read(config_path)
    check_config(config)
    if config.get(DEFAULT, "version") != __version__:
        config.set(DEFAULT, "version", __version__)
        write_config(config)
    return config


def check_config(config):
    """
    Checks config against default config for fields.

    Args:
        config: Configuration to write.
    """

    for key in default_config:
        try:
            config.get(DEFAULT, key)
        except NoOptionError:
            config.set(DEFAULT, key, default_config.get(key))
    write_config(config)
