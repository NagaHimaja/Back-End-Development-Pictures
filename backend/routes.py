from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data),200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((p for p in data if p['id'] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return "Picture not found", 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = request.json
    if not picture_data:
        return "Invalid request data", 400

    new_id = picture_data.get('id')
    picture = next((p for p in data if p['id'] == new_id), None)

    if picture:
        return {"Message": f"picture with id {picture['id']} already present"}, 302

    data.append(picture_data)
    return jsonify(picture_data), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    request_data=request.json 
    picture = next((i for i in data if i['id']==id),None)
    if picture:
        picture.update(request_data)
        return jsonify(picture), 200
    else:
        return {"message": "picture not found"}, 404
"""
Also we can use 
    if picture:
        # Update the existing picture data with the incoming request data
        for key, value in request_data.items():
            picture[key] = value
        return jsonify(picture), 200
without using built-in method

"""
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    request_data=next((i for i in data if i['id']==id),None)
    if request_data:
        data.remove(request_data)
        return '', 204
    else:
        return {"message": "picture not found"}, 404
