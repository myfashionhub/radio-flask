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
    target_url = request.form.get('url')
    link = find_or_create_short_url(target_url)
    short_url = config.DOMAIN + link.key
    return render_template('link.html', link=link, short_url=short_url)

@app.route('/<regex("[a-z0-9]{8}"):key>/')
def redirect_to_target(key):
    link = session.query(ShortUrl).filter(ShortUrl.key==key).first()
    if link == None:
        return render_template('404.html')
    else:
        save_click(link)
        return redirect(link.target_url)

@app.route('/links')
def links():
    links = []
    for short_url in session.query(ShortUrl).order_by(ShortUrl.created_at):
        links.append(short_url)
    return render_template('links.html', links=links, domain=config.DOMAIN)

@app.route('/link/<regex("[a-z0-9]{8}"):key>/')
def show_link(key):
    short_url = config.DOMAIN + key
    link      = session.query(ShortUrl) \
                .filter(ShortUrl.key==key) \
                .first()
    click_query = session.query(Click) \
                  .filter(Click.short_url_id==link.id) \
                  .order_by(Click.created_at)
    click_total = click_query.count()
    clicks      = click_query.all()

    return render_template(
               'link.html', link=link, short_url=short_url,
               click_total=click_total, clicks=clicks
           )

def find_or_create_short_url(target_url):
    link = session.query(ShortUrl) \
           .filter(ShortUrl.target_url==target_url) \
           .first()

    if link == None:
        key = str(uuid.uuid4())[:8]
        link = ShortUrl(
            key=key,
            target_url=target_url
        )
        session.add(link)
        session.commit()

    return link

def save_click(link):
    click = Click(short_url_id=link.id)
    session.add(click)
    session.commit()
