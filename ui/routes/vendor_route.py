from flask import Blueprint, render_template, request, jsonify
from http.api_client import api_get, api_post

vendor_bp = Blueprint("vendor", __name__, url_prefix="/vendor")

@vendor_bp.route("/")
def vendor_list():
    data = api_get("vendors/all")
    return render_template("dashboard.html", response=data)

@vendor_bp.route("/add", methods=["POST"])
def add_vendor():
    vendor_name = request.form.get("vendor_name")
    payload = {"vendor_name": vendor_name, "created_by": 1}
    result = api_post("vendors/create", payload)
    return jsonify(result)
