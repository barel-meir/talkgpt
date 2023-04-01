import logging
import os
from gui import Gui
from analyzer import Analyzer


def create_directory(path):
    """
    Create a directory path if it doesn't exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def init_logging():
    log_file_path = "~/.talkgpt/log"
    create_directory(log_file_path)
    log_file_name = "talk.log"
    file_path = os.path.join(log_file_path, log_file_name)

    # Create a logger and set its level to DEBUG
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler that writes to the specified log file
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a console handler that writes to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def initialize():
    init_logging()
    Analyzer.initialize()


def main():
    initialize()
    gui = Gui()
    gui.run()


if __name__ == '__main__':
    main()

