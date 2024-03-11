def init_app(app):
    app.config["TITLE"] = 'FarmaFlask'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
    app.config['SECRET_KEY'] = '123'
