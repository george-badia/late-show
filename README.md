# Late Show API

Welcome to the Late Show API project! This Python project uses Flask and SQLAlchemy to manage and serve data about episodes, guests, and appearances from a late-night talk show.

#### By **George Badia**

This project was created and is the sole property of george badia.

## Project Overview

The Late Show API models a talk show database with three primary entities:

- _Episode_: Represents a single episode of the show with a date and episode number.
- _Guest_: Represents a guest who has appeared on the show, including their name and occupation.
- _Appearance_: Represents the relationship between an episode and a guest, including a rating for the appearance.

### This project also simulates the relationships between these entities:

- An episode can have multiple guests through appearances.
- A guest can appear in multiple episodes.
- Each appearance belongs to one episode and one guest, with a rating.

## Features

- _Episode Management_: Retrieve all episodes or a single episode with its associated appearances.
- _Guest Management_: Retrieve all guests.
- _Appearance Management_: Create new appearances with ratings.
- _Data Validation_: Appearances require a rating between 1 and 5.
- _RESTful API_: The project follows REST conventions for managing episodes, guests, and appearances.

## Setup/Installation Requirements

- Linux or WSL for Windows users
- Visual Studio Code installed
- GitHub account
- Python 3.x

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/george-badia/late-show
   ```
2. Navigate to the repository directory:
   ```bash
   cd late-show
   ```
3. Open in Visual Studio Code or your preferred IDE:
   ```bash
   $ code .
   ```

## Running the Application

1. Ensure Python 3.x is installed on your machine.
2. Set up the virtual environment: This project uses pipenv for managing dependencies.
   ```bash
   $ pipenv install
   $ pipenv shell
   ```
3. Run the application:
   ```bash
   $ cd server
   $ python3 app.py
   ```

## Endpoints

### GET /episodes

List all episodes with their id, date, and number:

```json
[
  {
    "id": 1,
    "date": "1999-01-11",
    "number": 1
  },
  ...
]
```

### GET /episodes/:id

Retrieve a specific episode by its id, including its appearances:

```json
{
  "id": 1,
  "date": "1999-01-11",
  "number": 1,
  "appearances": [
    {
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      },
      "id": 1,
      "rating": 5,
      "guest_id": 1
    }
  ]
}
```

### GET /guests

List all guests:

```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  ...
]
```

### POST /appearances

Create a new appearance:

```json
{
  "rating": 5,
  "episode_id": 1,
  "guest_id": 1
}
```

## Technologies Used

This program is built with:

- Flask (for REST API)
- SQLAlchemy (for ORM)
- Python 3.x
- Visual Studio Code environment

## Support and Contact Details

For any issues, please email me at george.otieno1@student.moringaschool.com

## License

This project is licensed under the MIT License.
