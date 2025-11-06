from flask import Flask
from routes import register_routes

app = Flask(__name__)
app.secret_key = "invoai_secret_key"  # for sessions or CSRF if needed

# Register all route blueprints dynamically
register_routes(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
