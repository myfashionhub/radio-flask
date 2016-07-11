from werkzeug.routing import BaseConverter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jinja2 import Undefined
import random

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

DEVICE_TYPES = {
  'desktop': [ 'macos', 'windows', 'linux' ],
  'tablet': [ 'ipad' ],
  'mobile': [ 'iphone', 'android' ]
}


def sanitize_device(criteria):
    if criteria is None or isinstance(criteria, Undefined):
        return 'Default'

    return criteria.replace('device_type:', '').capitalize()


def random_short_url():
    sequence = 'abcdefghijklmnopqrstuvwxyz' + \
               'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
               '0123456789'
    url = ''
    for _ in range(6):
         url += random.choice(sequence)
    return url
