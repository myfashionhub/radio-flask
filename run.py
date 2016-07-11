import url_shortener
import logging
from url_shortener import config

if __name__ == '__main__':
    if config.DEBUG_MODE == True:
        logging.basicConfig(level=logging.DEBUG)

    url_shortener.app.run(host='0.0.0.0', debug=config.DEBUG_MODE)
