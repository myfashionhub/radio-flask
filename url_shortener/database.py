from sqlalchemy import create_engine
from application import create_session
from models import ShortUrl, Click
from config import DATABASE_URL
import uuid

class Database():
    def __init__(self):
        self.session = create_session(DATABASE_URL)

    def get_links_with_clicks(self, key):
        links = self.session.query(ShortUrl) \
                .filter(ShortUrl.key==key) \
                .all()
        link_ids = [link.id for link in links]
        click_query = self.session.query(Click) \
                      .filter(Click.short_url_id.in_(link_ids)) \
                      .order_by(Click.created_at)

        results = []
        for link in links:
            query = click_query.filter(Click.short_url_id==link.id)
            click_total = query.count()
            clicks      = query.all()
            results.append( {
                'link': link,
                'click_total': click_total,
                #clicks: clicks
            } )
        return results

    def find_or_create_short_url(self, target_url):
        link = self.session.query(ShortUrl) \
               .filter(ShortUrl.target_url==target_url) \
               .first()

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

    def query_clicks(self, link_ids):

        return [ click_total, clicks ]

    def add_target(self, key, target_url, device_type):
        link = ShortUrl(
            key=key,
            target_url=target_url,
            user_agent='device_type:' + device_type
        )
        self.session.add(link)
        self.session.commit()
        return link

