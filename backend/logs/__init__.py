from logging.config import dictConfig
import logging
from backend.core.config import settings

dictConfig(settings.LOGGING_CONFIG)
