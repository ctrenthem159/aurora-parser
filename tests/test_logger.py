import logging
import tempfile
import os
from app.logger import setup_logging

def test_setup_logging_console_only(monkeypatch):
    setup_logging()

    logger = logging.getLogger()
    assert logger.level == logging.INFO

    handlers = logger.handlers
    assert len(handlers) == 1
    assert isinstance(handlers[0], logging.StreamHandler)

    formatter = handlers[0].formatter
    assert formatter._fmt == "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

def test_setup_logging_with_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        log_file = tmp.name

    try:
        setup_logging(level=logging.WARNING, log_file=log_file)

        logger = logging.getLogger()
        assert logger.level == logging.WARNING

        handler_types = [type(h) for h in logger.handlers]
        assert logging.StreamHandler in handler_types
        assert logging.FileHandler in handler_types

        logger.warning("test log")
        logger.handlers[-1].flush()

        with open(log_file, "r") as f:
            content = f.read()
        assert "test log" in content
    finally:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
        os.remove(log_file)
