from flask.ext.assets import Bundle, Environment
from url_shortener import app

bundles = {

  'script': Bundle(
      'javascript/main.js',
      output='generated/script.js'
  ),

  'style': Bundle(
      'stylesheet/main.scss',
      filters='pyscss',
      output='generated/style.css'
  )
}

assets = Environment(app)
assets.register(bundles)
