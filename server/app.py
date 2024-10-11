# Import necessary modules and classes from Flask, Flask-RESTful, and SQLAlchemy
from flask import request, jsonify
from flask_restful import Resource
from models import db, Episode, Guest, Appearance
from flask import Flask
from flask_restful import Api, reqparse
from flask_migrate import Migrate

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///late_show.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Resource for handling multiple episodes
class EpisodeResource(Resource):
    def get(self):
        # Retrieve all episodes and return as a list of dictionaries
        episodes = Episode.query.all()
        data = [
            {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            }
            for episode in episodes
        ]
        return data, 200

# Resource for handling a single episode
class SingleEpisodeResource(Resource):
    def get(self, id):
        # Retrieve a specific episode by id
        episode = Episode.query.get(id)
        if episode:
            # If found, return episode data including appearances
            data = {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number,
                'appearances': [
                    {
                        'episode_id': appearance.episode_id,
                        'guest': {
                            'id': appearance.guest.id,
                            'name': appearance.guest.name,
                            'occupation': appearance.guest.occupation
                        },
                        'id': appearance.id,
                        'rating': appearance.rating,
                        'guest_id': appearance.guest_id,
                    }
                    for appearance in episode.appearances
                ]
            }
            return data, 200
        else:
            # If not found, return error
            return {'error': 'Episode not found'}, 404

    def delete(self, id):
        # Delete a specific episode by id
        episode = Episode.query.get(id)
        if episode:
            db.session.delete(episode)
            db.session.commit()
            return '', 204
        else:
            return {'error': 'Episode not found'}, 404
