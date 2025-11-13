from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    # Dummy response structure to prevent template errors
    response = {
        "response_status": False,
        "message": "No vendors found.",
        "source_output": []
    }
    return render_template("dashboard.html", response=response)
