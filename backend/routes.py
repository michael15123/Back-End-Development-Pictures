from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))



@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200



@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500



@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200



@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    
    for picture in data:
        if picture["id"] == id:
            return picture
    
    return {"message": "Picture not found"}, 404



@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    if new_picture in data:
        return {"Message": f"picture with id {new_picture['id']} already present"}, 302
    
    try:
        data.append(new_picture)
    except:
        return {"message": "data not defined"}, 500
    
    return {"id": new_picture['id']}, 201



@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_picture = request.json

    pos = 0
    for picture in data:
        if picture["id"] == update_picture["id"]:
            data[pos] = update_picture
            return {"message": picture}, 200
        pos += 1
    
    return {"message": "picture not found"}, 404


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return {"message": f"{id}"}, 204
    
    return {"message": "picture not found"}, 404
