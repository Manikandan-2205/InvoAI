from routes.dashboard_route import dashboard_bp
from routes.auth_route import auth_bp


def register_routes(app):

    # Register each blueprint with the app
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
