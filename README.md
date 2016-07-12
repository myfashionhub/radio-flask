URL Shortener
============

### Specs
- Using Python2, Flask


### Setting up
- Install requirements: `pip install -r requirements.txt`   
- Run the app: `python run.py`   
- Application is available at `localhost:5000`  

- The home page has a form that allows you to input target URLs and create short links. If the target URL is valid, a short URL is created, user is redirected to the edit page.

- On the edit page, user can add target URL to the current short link based on the device type (based on [Werkzeug's doc on platform types](http://werkzeug.pocoo.org/docs/0.11/utils/#module-werkzeug.useragents)).

- Clicking on the short URL on a desktop environment short increase the number of clicks under that target on refresh. The first target added is the default for types of device that don't have specified target.

- I tested on mobile devices by using the public IP instead of localhost. The number of clicks increased for the mobile target.

- "All my links" page has a list of all the short links created

### Testing
(The config setup is not perfect since I am new to Flask)
- Change `TEST_MODE` to `True` in `url_shortener/config.py`
- Run the test suite `py.test url_shortener/tests`
