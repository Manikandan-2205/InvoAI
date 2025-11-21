from flask import Blueprint, redirect, request, render_template, jsonify, session, url_for
from services.auth import remove_claims, set_claims
from api import vendor_client

vendor_bp = Blueprint("vendor", __name__, url_prefix="/vendor")


@vendor_bp.route("/get-all-vendors", methods=["GET", "POST"])
def get_all_vendors():
    return render_template("vendor/vendor_list.html")


@vendor_bp.route("/new-vendor", methods=["GET", "POST"])
def add_vendor():   
    if request.method == "POST":
        vendor_name = request.form.get("vendor_name")
        if not vendor_name:
            return jsonify({
                "isSuccess": False,
                "message": "Vendor name is required"
            }), 400
        result = vendor_client.add_vendor(vendor_name)
        if result.success:
            return jsonify({
                "isSuccess": True,
                "message": result.message,
                "url": "/vendor/get-all-vendors"
            }), 200
        else:
            return jsonify({
                "isSuccess": False,
                "message": result.message
            }), result.code

    return render_template("vendor/new_vendor.html")


@vendor_bp.route("/edit-vendor/<int:id>", methods=["GET", "POST"])
def edit_vendor(id: int = None):
    if request.method == "GET":
        if id is not None:
            result = vendor_client.get_vendor_by_id(id)
            if result.success:
                return render_template("vendor/new_vendor.html", vendor=result.data.get("vendor"))
            else:
                return jsonify({
                    "isSuccess": False,
                    "message": result.message
                }), result.code
        else:
            return render_template("vendor/new_vendor.html")
