import logging
import sys


def setup_logger() -> logging.Logger:
    """Configure et retourne le logger principal du projet."""
    logger = logging.getLogger("quote_optimizer")

    # Évite de réajouter des handlers si le logger est déjà configuré
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Format des messages : Horodatage | Niveau | Fichier:Ligne | Message
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. Handler Console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. Handler Fichier (app.log)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Instance globale
logger = setup_logger()
