import sys, os
from sqlalchemy import create_engine
app_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(app_path)

from database import Database
from application import random_short_url
from models import Base

class TestDatabase():
    def setup_class(self):
        db_file = 'url_shortener_test.db'
        db_url  = 'sqlite:///' + db_file
        if os.path.exists(db_file):
            os.remove(db_file)

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(engine)
        self.db = Database(db_url)

    def test_url_key_exists(self):
        key = random_short_url()
        assert self.db.url_key_exists(key) == False

        self.db.save_short_url(key, 'http://target-link.org')
        assert self.db.url_key_exists(key) == True

    def test_save_short_url(self):
        count1 = self.db.all_links().count()

        key = random_short_url()
        self.db.save_short_url(key, 'http://save-short-url.test')
        count2 = self.db.all_links().count()

        assert count2 - count1 == 1

    def test_find_or_create_short_url(self):
        # It locates the correct short url if it exists
        # It does not create a duplicate url

        key = random_short_url()
        target_url = 'http://target-video.com'
        link1 = self.db.save_short_url(key, target_url)
        count1 = self.db.all_links().count()

        link2 = self.db.find_or_create_short_url(target_url)
        count2 = self.db.all_links().count()

        assert link1 == link2
        assert count1 == count2

    def test_save_click(self):
        link = self.db.all_links().first()
        for i in range(5):
            self.db.save_click(link.id, 'http://referrer%s.net' % i)

        results = self.db.get_links_with_clicks(link.key)
        assert results[0]['click_total'] == 5

    def test_query_target(self):
        link1 = self.db.all_links().first()
        link2 = self.db.save_short_url(
                    link1.key, 'http://new-target.com', 'device_type:desktop'
                )
        link3 = self.db.query_target(link1.key, 'macos')
        assert link3 == link2

        link4 = self.db.query_target(link1.key, 'wii')
        assert link4 == link1
