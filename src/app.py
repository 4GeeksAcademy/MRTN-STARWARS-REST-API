"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import User, Character, Planet, FavoriteCharacter, FavoritePlanet, db
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planet', methods= ['GET'])
def planet():
    planets = Planet.query.all()
    planets_list = [planets.serialize() for planets in planets]
    return jsonify(planets_list), 200
    
@app.route('/character', methods= ['GET'])
def character():
    characters = Character.query.all()
    character_list = [characters.serialize() for characters in characters]
    return jsonify(character_list), 200

@app.route('/user/<int:user_id>/favorite_characters', methods=['GET'])
def get_user_favorite_characters(user_id):
    user = User.query.get(user_id)
    if user:
        favorite_characters = FavoriteCharacter.query.filter_by(user_id=user.id)
        character_list = [fav.serialize() for fav in favorite_characters]
        return jsonify(character_list), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Ruta para agregar un personaje a la lista de favoritos de un usuario
@app.route('/user/<int:user_id>/favorite_characters', methods=['POST'])
def add_favorite_character(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        character_id = data.get("character_id")
        if character_id:
            character = Character.query.get(character_id)
            if character:
                favorite_character = FavoriteCharacter(user_id=user.id, character_id=character.id)
                db.session.add(favorite_character)
                db.session.commit()
                return jsonify({"message": "Personaje agregado a favoritos"}), 201
            else:
                return jsonify({"message": "Personaje no encontrado"}), 404
        else:
            return jsonify({"message": "ID de personaje no proporcionado"}), 400
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Ruta para eliminar un personaje de la lista de favoritos de un usuario
@app.route('/user/<int:user_id>/favorite_characters/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if user:
        favorite_character = FavoriteCharacter.query.filter_by(user_id=user.id, character_id=character_id).first()
        if favorite_character:
            db.session.delete(favorite_character)
            db.session.commit()
            return jsonify({"message": "Personaje eliminado de favoritos"}), 200
        else:
            return jsonify({"message": "Personaje no encontrado en la lista de favoritos"}), 404
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

@app.route('/user/<int:user_id>/favorite_planets', methods=['GET'])   
def get_user_favorite_planets(user_id):
    user = User.query.get(user_id)
    if user:
        favorite_planets = FavoritePlanet.query.filter_by(user_id=user.id)
        planet_list = [fav.serialize() for fav in favorite_planets]
        return jsonify(planet_list), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Ruta para agregar un planeta a la lista de favoritos de un usuario
@app.route('/user/<int:user_id>/favorite_planets', methods=['POST'])
def add_favorite_planet(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        planet_id = data.get("planet_id")
        if planet_id:
            planet = Planet.query.get(planet_id)
            if planet:
                favorite_planet = FavoritePlanet(user_id=user.id, planet_id=planet.id)
                db.session.add(favorite_planet)
                db.session.commit()
                return jsonify({"message": "Planeta agregado a favoritos"}), 201
            else:
                return jsonify({"message": "Planeta no encontrado"}), 404
        else:
            return jsonify({"message": "ID de planeta no proporcionado"}), 400
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Ruta para eliminar un planeta de la lista de favoritos de un usuario
@app.route('/user/<int:user_id>/favorite_planets/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if user:
        favorite_planet = FavoritePlanet.query.filter_by(user_id=user.id, planet_id=planet_id).first()
        if favorite_planet:
            db.session.delete(favorite_planet)
            db.session.commit()
            return jsonify({"message": "Planeta eliminado de favoritos"}), 200
        else:
            return jsonify({"message": "Planeta no encontrado en la lista de favoritos"}), 404
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
