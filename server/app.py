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

# Resource for handling guests
class GuestResource(Resource):
    def get(self):
        # Retrieve all guests and return as a list of dictionaries
        guests = Guest.query.all()
        data = [
            {
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            }
            for guest in guests
        ]
        return data, 200

# Resource for handling appearances
class AppearanceResource(Resource):
    # Set up request parser for POST requests
    parser = reqparse.RequestParser()
    parser.add_argument('rating', type=int, required=True)
    parser.add_argument('episode_id', type=int, required=True)
    parser.add_argument('guest_id', type=int, required=True)

    def post(self):
        # Parse arguments from the request
        args = self.parser.parse_args()
        rating = args['rating']
        episode_id = args['episode_id']
        guest_id = args['guest_id']

        # Retrieve episode and guest
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)

        # Check if episode and guest exist
        if not episode:
            return {'error': 'Episode not found'}, 404
        if not guest:
            return {'error': 'Guest not found'}, 404

        # Validate rating
        if not (1 <= rating <= 5):
            return {'errors': ['Validation error. Rating must be between 1 and 5 (inclusive).']}, 400

        # Create new appearance
        appearance = Appearance(rating=rating, episode=episode, guest=guest)
        db.session.add(appearance)
        db.session.commit()

        # Prepare and return response
        response_data = {
            'id': appearance.id,
            'rating': appearance.rating,
            'guest_id': guest.id,
            'episode_id': episode.id,
            'episode': {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            },
            'guest': {
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            }
        }
        return response_data, 201

# Add resources to API
api.add_resource(EpisodeResource, '/episodes')
api.add_resource(SingleEpisodeResource, '/episodes/<int:id>')
api.add_resource(GuestResource, '/guests')
api.add_resource(AppearanceResource, '/appearances')

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)