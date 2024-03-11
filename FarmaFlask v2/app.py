from os.path import join, dirname, realpath

from flask import Flask

import views
from ext import database, configuracao

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/product_images')


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    configuracao.init_app(app)
    database.init_app(app)
    views.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
