# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:53:35 2024

@author: DeepanshuBalani
"""

import logging

def setup_logging(log_file_path, log_level=logging.INFO):
    """
    Set up logging to a file using the root logger and return it.

    Args:
        log_file_path (str): Path to the log file.
        log_level (int): Log level (default is logging.INFO).

    Returns:
        logging.Logger: Root logger instance.
    """
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Add the file handler to the root logger
    root_logger.addHandler(file_handler)

    return root_logger

