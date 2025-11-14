from flask import Flask
from routes.register_routes import register_routes
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

register_routes(app)
if __name__ == "__main__":
    app.run(port=5000, debug=True)
