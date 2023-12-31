import logging
import os

import configmap

confmap = configmap.Config("configfiles/", ["config.yaml"])
confmap.load_config()
config = confmap.config
if os.getenv('LOCAL'):
    confmap = configmap.Config("configfiles/", ["local_config.yaml"])
    confmap.load_config()
    config = confmap.local_config

logging.basicConfig(format=config.log.format, level=config.log.level)