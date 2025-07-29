import logging


class Logger:
    def __init__(self, name: str = "default_logger", level: str = "DEBUG"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid adding multiple handlers if logger already initialized
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
            )
            self.logger.addHandler(console_handler)

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def set_level(self, level: int):
        self.logger.setLevel(level)
