from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
import logging
from application import DEVICE_TYPES, random_short_url
from models import ShortUrl, Click

def create_session(database_url):
    engine  = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session

class Database():
    def __init__(self, database_url):
        self.database_url = database_url
        self.session = create_session(database_url)

    def get_links_with_clicks(self, key):
        links = self.session.query(ShortUrl).filter_by(key=key).all()
        link_ids = [link.id for link in links]

        click_query = self.session.query(Click) \
                      .filter(Click.short_url_id.in_(link_ids)) \
                      .order_by(Click.created_at)

        results = []
        for link in links:
            query = click_query.filter_by(short_url_id=link.id)
            results.append( {
                'link': link,
                'click_total': query.count()
            } )
        return results

    def find_or_create_short_url(self, target_url):
        link = self.session.query(ShortUrl) \
               .filter_by(target_url=target_url).first()

        if link == None:
            key = random_short_url()
            while self.url_key_exists(key):
                key = random_short_url()
            link = self.save_short_url(key, target_url)
        return link

    def save_click(self, link_id, referrer_url):
        click = Click(
            short_url_id=link_id,
            referrer_url=referrer_url
        )
        self.session.add(click)
        self.session.commit()
        return click

    def save_short_url(self, key, target_url, criteria=None):
        link = ShortUrl(
            key=key,
            target_url=target_url,
            criteria=criteria
        )
        self.session.add(link)
        self.session.commit()
        return link

    def query_target(self, key, platform):
        device_type = None

        for type in DEVICE_TYPES:
            if platform in DEVICE_TYPES[type]:
                device_type = type
                break

        link_query = self.session.query(ShortUrl).filter_by(key=key)
        if device_type != None:
            link = link_query \
                   .filter(ShortUrl.criteria=='device_type:'+device_type) \
                   .first()

        if device_type == None or link == None:
            link = link_query.filter(ShortUrl.criteria==None).first()

        return link

    def all_links(self):
        links = self.session.query(ShortUrl).order_by(ShortUrl.created_at)
        return links

    def url_key_exists(self, key):
        link = self.session.query(ShortUrl).filter_by(key=key).first()
        return link != None
