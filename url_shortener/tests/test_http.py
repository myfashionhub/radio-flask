import sys, os
from multiprocessing import Process
import requests
import logging
from sqlalchemy import create_engine
from .. import app

app_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(app_path)

from database import Database
from application import random_short_url
from models import Base, ShortUrl, Click

def run_app():
    app.run(host='0.0.0.0', port=8000, debug=False)

class TestHttp():
    def setup_class(self):
        self.db_url  = app.config['DATABASE_URL_TEST']
        db_file = self.db_url.replace('sqlite:///', '')
        if os.path.exists(db_file):
            os.remove(db_file)

        engine = create_engine(self.db_url, echo=False)
        Base.metadata.create_all(engine)

        self.db = Database(self.db_url)
        self.base_url = app.config['BASE_URL_TEST']
        self.proc = Process(target=run_app)
        self.proc.start()

    def teardown_class(self):
        self.proc.terminate()

    def test_index(self):
        response = requests.get(self.base_url)
        assert response.status_code == 200
        assert 'Paste a URL to shorten' in response.text

    def test_shorten(self):
        target_url = 'http://www.nessanguyen.com/'
        endpoint = self.base_url + 'shorten'

        data = { 'url': target_url }
        response = requests.post(endpoint, data=data)

        link = self.db.find_or_create_short_url(target_url)
        expected_url = self.base_url + 'link/' + link.key + '/'

        assert response.history[-1].status_code == 301
        assert response.url == expected_url

    def test_redirect_to_target(self):
        link = self.db.all_links().first()
        response = requests.get(self.base_url + link.key)

        assert response.url == link.target_url
        assert response.history[-1].status_code == 302
