import csv
from datetime import datetime
from app import app, db
from models import Episode, Guest, Appearance

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Read CSV data
        with open('seed.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            
            episodes = {}
            guests = {}

            for row in csv_reader:
                # Create or get Episode
                date = datetime.strptime(row['Show'], '%m/%d/%y').date()
                if date not in episodes:
                    episode = Episode(date=date.strftime('%Y-%m-%d'), number=len(episodes) + 1)
                    db.session.add(episode)
                    episodes[date] = episode
                else:
                    episode = episodes[date]

                # Create or get Guest
                guest_name = row['Raw_Guest_List']
                if guest_name not in guests:
                    guest = Guest(name=guest_name, occupation=row['GoogleKnowlege_Occupation'])
                    db.session.add(guest)
                    guests[guest_name] = guest
                else:
                    guest = guests[guest_name]

                # Create Appearance
                appearance = Appearance(episode=episode, guest=guest, rating=3)  # Default rating
                db.session.add(appearance)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()