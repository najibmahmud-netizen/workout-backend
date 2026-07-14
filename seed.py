#!/usr/bin/env python3
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    db.create_all()

    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding Exercises...")
    ex1 = Exercise(name="Push Up", category="Strength", equipment_needed=False)
    ex2 = Exercise(name="Treadmill Sprint", category="Cardio", equipment_needed=True)
    ex3 = Exercise(name="Yoga Stretching", category="Flexibility", equipment_needed=False)
    
    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    print("Seeding Workouts...")
    w1 = Workout(date=date(2023, 10, 15), duration_minutes=45, notes="Felt great today!")
    w2 = Workout(date=date(2023, 10, 16), duration_minutes=30, notes="Quick cardio session.")
    
    db.session.add_all([w1, w2])
    db.session.commit()

    print("Seeding Workout Exercises (Join Table)...")
    # Adding Push Ups to Workout 1
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, reps=15, sets=3)
    # Adding Treadmill Sprints to Workout 1
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex2.id, duration_seconds=600)
    # Adding Yoga to Workout 2
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex3.id, duration_seconds=1200)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeded successfully!")