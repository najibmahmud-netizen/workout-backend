from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True) # dump_only means this is only sent OUT, never expected IN
    name = fields.Str(required=True)
    
    # SCHEMA VALIDATION 1: validate.OneOf restricts category to a specific list of acceptable values
    category = fields.Str(required=True, validate=validate.OneOf(
        ["Cardio", "Strength", "Flexibility", "Balance"], 
        error="Category must be Cardio, Strength, Flexibility, or Balance."
    ))
    equipment_needed = fields.Bool(required=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=False)
    exercise_id = fields.Int(required=False)
    reps = fields.Int()
    sets = fields.Int()
    
    # SCHEMA VALIDATION 2: validate.Range ensures duration doesn't go below 1 or absurdly high
    duration_seconds = fields.Int(validate=validate.Range(min=1, max=3600))
    
    # Nested schema to display the actual exercise details when viewing a workout
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()
    
    # Nested schema to include all the join table data (reps/sets) and the exercises
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

# Initialize schema instances for use in our routes
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()