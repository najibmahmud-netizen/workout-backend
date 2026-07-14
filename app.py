from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import datetime

from models import db, Exercise, Workout, WorkoutExercise
from schemas import exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

with app.app_context():
    db.create_all()

# --- ERROR HANDLING ---
# This global error handler catches any Marshmallow validation errors 
# and returns a clean 400 Bad Request to the user.
@app.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400

# --- EXERCISE ENDPOINTS ---

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    # Serialize the list of objects to JSON
    return exercises_schema.dump(exercises), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.dump(exercise), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    # .load() deserializes the JSON request and applies Schema Validations
    data = exercise_schema.load(request.json)
    
    try:
        new_exercise = Exercise(**data) # Model Validations run here
        db.session.add(new_exercise)
        db.session.commit() # Table Constraints run here
        return exercise_schema.dump(new_exercise), 201
    except ValueError as e: # Catches Model Validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e: # Catches Database constraints (like Unique Name violation)
        db.session.rollback()
        return jsonify({"error": "Failed to create exercise. Name might already exist."}), 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return '', 204 # 204 No Content is standard for successful deletions

# --- WORKOUT ENDPOINTS ---

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    # Thanks to our Nested schemas, this will automatically include reps/sets/duration data! (Stretch goal achieved)
    return workout_schema.dump(workout), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = workout_schema.load(request.json)
    try:
        new_workout = Workout(**data)
        db.session.add(new_workout)
        db.session.commit()
        return workout_schema.dump(new_workout), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    # Thanks to cascade="all, delete-orphan" in our models, associated WorkoutExercises are automatically deleted! (Stretch goal achieved)
    return '', 204

# --- JOIN TABLE ENDPOINT ---

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    # Verify both exist first
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)

    # Validate incoming join table data (reps, sets, etc.)
    data = workout_exercise_schema.load(request.get_json(silent=True) or {})
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id
    
    new_workout_exercise = WorkoutExercise(
        workout_id=data['workout_id'],
        exercise_id=data['exercise_id'],
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    
    db.session.add(new_workout_exercise)
    db.session.commit()
    
    return workout_exercise_schema.dump(new_workout_exercise), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)