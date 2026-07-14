from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

# We define naming conventions for constraints. This is a best practice 
# that helps Flask-Migrate generate correct migration scripts when altering tables.
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    # TABLE CONSTRAINT 1: unique=True ensures no two exercises can have the exact same name
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Relationship: One Exercise has many WorkoutExercises
    # cascade="all, delete-orphan" ensures if an exercise is deleted, its join table entries are too.
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade="all, delete-orphan")

    # MODEL VALIDATION 1: Ensure the exercise name is not empty or too short
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return name.strip().title() # Automatically capitalizes the name nicely

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # TABLE CONSTRAINT 2: CheckConstraint ensures duration is always a positive number
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='check_positive_duration'),
    )

    # Relationship: One Workout has many WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade="all, delete-orphan")

    # MODEL VALIDATION 2: Ensure notes do not exceed a reasonable length if provided
    @validates('notes')
    def validate_notes(self, key, notes):
        if notes and len(notes) > 500:
            raise ValueError("Notes cannot exceed 500 characters.")
        return notes

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Relationships back to the parent tables
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')