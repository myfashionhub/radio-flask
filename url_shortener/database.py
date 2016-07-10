from sqlalchemy import create_engine
from application import create_session
from models import ShortUrl, Click
from config import DATABASE_URL
import uuid

class Database():
    def __init__(self):
        self.session = create_session(DATABASE_URL)

    def get_link(self, key):
        return self.session.query(ShortUrl) \
               .filter(ShortUrl.key==key) \
               .first()

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

    def save_click(self, link_id):
        click = Click(short_url_id=link_id)
        self.session.add(click)
        self.session.commit()

    def query_clicks(self, link_id):
        click_query = self.session.query(Click) \
                      .filter(Click.short_url_id==link_id) \
                      .order_by(Click.created_at)
        click_total = click_query.count()
        clicks      = click_query.all()
        return [ click_total, clicks ]
