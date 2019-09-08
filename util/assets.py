# myapp/util/assets.py

from flask_assets import Bundle, Environment
from .. import app

bundles = {

    'home_js': Bundle(
        'static/js/lib/chartist.js',
        'static/js/lib/chartist.min.js',
        output='gen/home.js'),

    'home_css': Bundle(
        'static/css/lib/chartist.css',
        'static/css/lib/chartist.min.css',
        output='gen/home.css'),

}

assets = Environment(app)

assets.register(bundles)
