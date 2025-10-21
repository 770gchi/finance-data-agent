import logging
import os
from pathlib import Path

def get_logger(name: str = "fda", log_dir: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        if log_dir:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(os.path.join(log_dir, "run.log"))
            fh.setLevel(logging.INFO)
            fh.setFormatter(fmt)
            logger.addHandler(fh)
    return logger