from flask import Blueprint, render_template
from services.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/index")
@login_required
def dashboard():
    print("testing")
    return render_template("layout/dashboard.html")
