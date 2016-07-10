from werkzeug.routing import BaseConverter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def create_session(database_url):
    engine  = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session 
