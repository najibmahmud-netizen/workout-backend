# Workout Backend

A Flask-based backend API for managing workouts and exercises. The app uses Flask-SQLAlchemy, Flask-Migrate, and Marshmallow to provide validated models, relationships, and REST endpoints.

## Features

- Manage exercises with validation and uniqueness rules
- Manage workouts with duration and note validation
- Link exercises to workouts through a join table
- Seed starter data for local development
- Expose JSON endpoints for CRUD-style operations

## Setup

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install Flask==2.2.2 Flask-Migrate==3.1.0 flask-sqlalchemy==3.0.3 Werkzeug==2.2.2 importlib-metadata==6.0.0 importlib-resources==5.10.0 ipdb==0.13.9 marshmallow==3.20.1
   ```
3. Run the app:
   ```bash
   cd server
   python app.py
   ```

## Database setup

Initialize and seed the database:

```bash
cd server
python seed.py
```

## Main endpoints

- GET /exercises
- POST /exercises
- GET /workouts
- POST /workouts
- POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
