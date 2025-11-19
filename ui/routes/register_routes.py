from datetime import datetime
from routes.dashboard_route import dashboard_bp
from routes.auth_route import auth_bp
from routes.vendor_route import vendor_bp
from flask import redirect, url_for


def register_routes(app):

    @app.route("/")
    def home():
        return redirect(url_for("dashboard.dashboard"))

    @app.context_processor
    def inject_now():
        # Pass the RESULT (the object).
        return {'now': datetime.now()}
        

    # Register each blueprint with the app
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(vendor_bp)
