import unittest
from datetime import date

from app import app, db
from models import Exercise, Workout


class WorkoutApiTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            exercise = Exercise(name='Burpee', category='Cardio', equipment_needed=True)
            workout = Workout(date=date(2026, 7, 14), duration_minutes=40, notes='Test workout')
            db.session.add_all([exercise, workout])
            db.session.commit()
            self.exercise_id = exercise.id
            self.workout_id = workout.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_exercise_to_workout_accepts_url_ids(self):
        response = self.client.post(
            f'/workouts/{self.workout_id}/exercises/{self.exercise_id}/workout_exercises',
            json={'reps': 10, 'sets': 2, 'duration_seconds': 300}
        )

        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
