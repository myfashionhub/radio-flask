from sqlalchemy import create_engine
import uuid
import logging
from application import create_session, DEVICE_TYPES
from models import ShortUrl, Click
from config import DATABASE_URL

class Database():
    def __init__(self):
        self.session = create_session(DATABASE_URL)

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
            key = str(uuid.uuid4())[:8]
            link = ShortUrl(
                key=key,
                target_url=target_url
            )
            self.session.add(link)
            self.session.commit()

        return link

    def save_click(self, link_id, referrer_url):
        click = Click(
            short_url_id=link_id,
            referrer_url=referrer_url
        )
        self.session.add(click)
        self.session.commit()

    def add_target(self, key, target_url, device_type):
        link = ShortUrl(
            key=key,
            target_url=target_url,
            criteria='device_type:' + device_type
        )
        self.session.add(link)
        self.session.commit()
        return link

    def query_target(self, user_agent, key):
        platform = user_agent.platform
        device_type = None

        for type in DEVICE_TYPES:
            if platform in DEVICE_TYPES[type]:
                device_type = type

        link_query = self.session.query(ShortUrl).filter_by(key=key)
        if device_type != None:
            link = link_query \
                   .filter(ShortUrl.criteria=='device_type:'+device_type) \
                   .first()

        if device_type == None or link == None:
            link = link_query.filter(ShortUrl.criteria=='').first()

        return link
