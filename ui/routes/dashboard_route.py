from flask import Blueprint, render_template
from http.api_client import api_get

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    data = api_get("vendors/all")
    return render_template("dashboard.html", response=data)
