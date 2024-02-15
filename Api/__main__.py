import logging

from .routes.core import *
from .routes.plugins import *
from . import app

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


if __name__ == "__main__":
    # app.clear_all_routes()
    setup_logger()
    app.run(host="0.0.0.0", debug=True, port=80)
