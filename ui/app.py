from flask import Flask, render_template, request, jsonify
from http.api_client import api_get, api_post

app = Flask(__name__)

@app.route("/")
def index():
    data = api_get("vendors/all")
    return render_template("dashboard.html", response=data)

@app.route("/add-vendor", methods=["POST"])
def add_vendor():
    vendor_name = request.form.get("vendor_name")
    payload = {"vendor_name": vendor_name, "created_by": 1}
    result = api_post("vendors/create", payload)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
