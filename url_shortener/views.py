from flask import render_template, redirect, request
import logging
from url_shortener import app
from models import ShortUrl, Click
import config
from application import RegexConverter, create_session
from database import Database


app.url_map.converters['regex'] = RegexConverter
db_session = create_session(config.DATABASE_URL)
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    target_url  = request.form.get('url')
    key         = request.form.get('key')
    device_type = request.form.get('device_type')

    if key == None:
        link = db.find_or_create_short_url(target_url)
    else:
        link = db.add_target(key, target_url, device_type)

    short_url  = config.DOMAIN + link.key
    return render_template('link.html', link=link, short_url=short_url)

@app.route('/<regex("[a-z0-9]{8}"):key>/')
def redirect_to_target(key):
    link = db.identify_target(request.user_agent, key)
    if link == None:
        return render_template('404.html')
    else:
        db.save_click(link.id, request.referrer)
        return redirect(link.target_url)

@app.route('/links')
def links():
    links = db_session.query(ShortUrl).order_by(ShortUrl.created_at)
    return render_template('links.html', links=links, domain=config.DOMAIN)

@app.route('/link/<regex("[a-z0-9]{8}"):key>/')
def show_link(key):
    short_url = config.DOMAIN + key
    results   = db.get_links_with_clicks(key)

    return render_template( 'link.html', results=results, short_url=short_url )
