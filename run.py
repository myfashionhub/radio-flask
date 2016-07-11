from sqlalchemy import create_engine
import logging
from url_shortener import config, app, models

if __name__ == '__main__':
    if config.DEBUG_MODE == True:
        logging.basicConfig(level=logging.DEBUG)

    engine = create_engine(app.config['DATABASE_URL'], echo=False)
    models.Base.metadata.create_all(engine) # Run migration
    app.run(host='0.0.0.0', debug=config.DEBUG_MODE)
