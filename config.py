import importlib
import os
import sys
from logging import getLogger

TG_TOKEN="1733733262:AAF7z4PAe7Vt7d9KoVqptcPOpRCHxiONzwA"
logger = getLogger(__name__)

FEEDBACK_USER_ID = 840146543

def load_config():
    conf_name = os.environ.get("TG_CONF")
    if conf_name is None:
        conf_name = "production"
    try:
        r = importlib.import_module("settings.{}".format(conf_name))
        logger.debug("Loaded config \"{}\" - OK".format(conf_name))
        return r
    except (TypeError, ValueError, ImportError):
        logger.error("Invalid config \"{}\"".format(conf_name))
        sys.exit(1)
