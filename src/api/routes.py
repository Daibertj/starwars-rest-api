"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet, Favorite
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)



@api.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()

    users= list(map(lambda item:item.serialize(), users))
    return jsonify(users)

@api.route('/people', methods=['GET'])
def get_people():

    characters = Character.query.all()

    people = []
    for character in characters:
        people.append(character.serialize())
    return jsonify(people)

@api.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()

    planets = list(map(lambda item:item.serialize(), planets))
    return jsonify(planets)

@api.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):

    character = Character.query.filter_by(id = people_id).first()
    if character is None:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(character.serialize())

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.filter_by(id = planet_id).first()
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize())

@api.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['POST'])
def add_fav_people(people_id, user_id):

    favorite = Favorite.query.filter_by(character_id = people_id, user_id = user_id).first()
    
    if favorite is not None:
        return jsonify({"msg": "Character it is already added"}), 400
    fav = Favorite(character_id = people_id, user_id = user_id)
    db.session.add(fav)
    try:
        db.session.commit()
        return jsonify(fav.serialize()), 201
    except Exception as error:
        return jsonify({"msg": error.args}), 500

@api.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_fav_planets(planet_id, user_id):

    favorite = Favorite.query.filter_by(planet_id = planet_id, user_id = user_id).first()

    if favorite is not None:
        return jsonify({"msg": "Planet it is already added"}), 400
    fav = Favorite(planet_id = planet_id, user_id = user_id)
    db.session.add(fav)
    try:
        db.session.commit()
        return jsonify(fav.serialize()), 201
    except Exception as error:
        return jsonify({"msg": error.args}), 500

@api.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['DELETE'])
def delete_fav_people(people_id, user_id):

    favorite = Favorite.query.filter_by(character_id = people_id, user_id = user_id).first()

    if favorite is None:
        return jsonify({"msg": "Character does not exist"}), 400
    db.session.delete(favorite)
    try:
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    except Exception as error:
        return jsonify({"msg": error.args}), 500

@api.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_fav_planets(planet_id, user_id):

    favorite = Favorite.query.filter_by(planet_id = planet_id, user_id = user_id).first()

    if favorite is None:
        return jsonify({"msg": "Planet does not exist"}), 400
    db.session.delete(favorite)
    try:
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    except Exception as error:
        return jsonify({"msg": error.args}), 500


@api.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_all_fav(user_id):

    favorite = Favorite.query.filter_by(user_id = user_id).all()
    favorites= list(map(lambda item:item.serialize(), favorite))
    return jsonify(favorites)

