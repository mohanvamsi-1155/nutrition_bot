import logging


class Logger:
    def __init__(self, name: str = "default_logger", level: str = "DEBUG"):
        self.log = logging.getLogger(name)
        self.log.setLevel(level)

        # Avoid adding multiple handlers if logger already initialized
        if not self.log.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
            )
            self.log.addHandler(console_handler)

    def info(self, msg: str, *args, **kwargs):
        self.log.info(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self.log.debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.log.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.log.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        self.log.exception(msg, *args, **kwargs)

    def set_level(self, level: int):
        self.log.setLevel(level)
