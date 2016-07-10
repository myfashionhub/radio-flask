from flask import render_template, redirect, request, session, flash, url_for
from url_shortener import app
import uuid
from sqlalchemy import create_engine
from models import ShortUrl, Click
import config
from application import RegexConverter, create_session


app.url_map.converters['regex'] = RegexConverter
session = create_session(config.DATABASE_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    target_url = request.args.get('url')
    key = save_short_url(target_url)
    short_url = config.DOMAIN + key
    return render_template('link.html', url=short_url)

@app.route('/<regex("[a-z0-9]{8}"):key>/')
def redirect_to_target(key):
    link = session.query(ShortUrl).filter(ShortUrl.key==key).first()
    if link == None:
        return render_template('404.html')
    else:
        return redirect(link.target_url)

def save_short_url(target_url):
    key = str(uuid.uuid4())[:8]
    short_url = ShortUrl(
      key=key,
      target_url=target_url
    )
    session.add(short_url)
    session.commit()
    print "Saving short URL %s" % key
    return key

@app.route('/links')
def links():
    links = []
    for short_url in session.query(ShortUrl).order_by(ShortUrl.created_at):
        links.append(short_url)
    return render_template('links.html', links=links, domain=config.DOMAIN)
