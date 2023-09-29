import logging

import yaml
from easydict import EasyDict
import inotify.adapters

class Config:
    def __init__(self, path, files, on_load=None):
        self.inotify = inotify.adapters.Inotify()
        self.path = path
        self.files = files
        self.on_load = on_load
        self.log = logging.getLogger()
        self.log.setLevel("INFO")

    def load_config(self, load_name=None):
        """
        Загрузить все файлы или указанный
        :param load_name:
        """
        for name in self.files:
            if load_name is not None and name != load_name:
                continue
            self.log.debug(f"Load configfile '{name}'")
            with open(f"{self.path}{name}") as file:
                _config = yaml.safe_load(file)
            cfg = EasyDict(_config)
            setattr(self, name.split('.')[0], cfg)
            if self.on_load is not None:
                self.on_load(name, cfg)
