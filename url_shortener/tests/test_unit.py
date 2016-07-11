import sys, os
import re
app_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(app_path)

from application import random_short_url


def test_length():
    url_key = random_short_url()
    assert len(url_key) == 6

def test_composition():
    url_key = random_short_url()
    match = re.match('[a-zA-Z0-9]{6}', url_key)
    assert match.group(0) == url_key

def test_uniqueness():
    urls = {}
    for _ in range(1000):
        key = random_short_url()
        assert key not in urls
        urls[key] = 1
