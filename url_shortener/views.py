from flask import render_template, redirect, request, session, flash, url_for
from url_shortener import app
import json

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/shorten')
def shorten():
  target_url = request.args.get('url')
  return render_template('links.html')
