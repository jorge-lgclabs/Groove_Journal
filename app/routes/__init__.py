from .routes import api_blueprint, main_blueprint


def register_routes(app):
    app.register_blueprint(api_blueprint)
    app.register_blueprint(main_blueprint)
