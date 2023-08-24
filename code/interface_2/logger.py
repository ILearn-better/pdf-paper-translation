import logging
from logging.handlers import RotatingFileHandler
import os


def create_logger(log_file, log_level=logging.INFO):
    # 创建一个日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # 设置日志记录器的级别，例如INFO、DEBUG、WARNING等
    if not os.path.exists("log"):
        os.mkdir("log")
    log_handler = RotatingFileHandler(os.path.join("log", 'app.log'), maxBytes=10240, backupCount=10)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    return logger


# 使用封装的函数来创建日志记录器
logger = create_logger(os.path.join('log', 'app.log'))
