# tests/test_models.py

import unittest
from sqlalchemy import create_engine
from datetime import date, datetime
from sqlalchemy.orm import sessionmaker
from app.models.tables import (
    Base,
    User,
    WorkoutLog,
    NutritionLog,
    SleepLog,
    HealthMetrics,
    HeightLog,
    WeightLog,
    HeartRateLog,
    WaterIntakeLog,
    UserFitnessGoal,
)  # noqa


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def create_user(self, username, age, email):
        user = User(username=username, age=age, email=email)
        self.session.add(user)
        self.session.commit()
        return user

    def test_user_creation(self):
        self.create_user(username="testuser", age=25, email="test@mail.com")

        retrieved_user = self.session.query(User).filter_by(username="testuser").one()
        self.assertEqual(retrieved_user.email, "test@mail.com")
        self.assertEqual(retrieved_user.age, 25)

    def test_height_log_creation(self):
        user = self.create_user("heightuser", 30, "height@example.com")

        height_log = HeightLog(
            user_id=user.id,
            date_recorded=date(2021, 1, 1),
            height=180.0,
        )
        self.session.add(height_log)
        self.session.commit()

        retrieved_log = self.session.query(HeightLog).filter_by(user_id=user.id).one()
        self.assertEqual(retrieved_log.height, 180.0)

    def test_weight_log_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        weight_log = WeightLog(
            user_id=user.id, date_recorded=date(2021, 1, 1), weight=80.0
        )
        self.session.add(weight_log)
        self.session.commit()

        retrieved_log = self.session.query(WeightLog).filter_by(user_id=user.id).one()
        self.assertEqual(retrieved_log.weight, 80.0)

    def test_workout_log_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        workout_log = WorkoutLog(
            user_id=user.id,
            date=date(2021, 1, 1),
            exercise_type="Running",
            duration=60.0,
        )
        self.session.add(workout_log)
        self.session.commit()

        retrieved_log = self.session.query(WorkoutLog).filter_by(user_id=user.id).one()
        self.assertEqual(retrieved_log.exercise_type, "Running")
        self.assertEqual(retrieved_log.duration, 60.0)

    def test_water_intake_log_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        water_intake_log = WaterIntakeLog(
            user_id=user.id,
            date=date(2021, 1, 1),
            water_intake=1000,
        )
        self.session.add(water_intake_log)
        self.session.commit()

        retrieved_log = (
            self.session.query(WaterIntakeLog).filter_by(user_id=user.id).one()
        )
        self.assertEqual(retrieved_log.water_intake, 1000)

    def test_nutrition_log_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        nutrition_log = NutritionLog(
            user_id=user.id,
            date=date(2021, 1, 1),
            food="Pizza",
            calories=1000,
            meal_type_id=1,
        )
        self.session.add(nutrition_log)
        self.session.commit()

        retrieved_log = (
            self.session.query(NutritionLog).filter_by(user_id=user.id).one()
        )
        self.assertEqual(retrieved_log.food, "Pizza")
        self.assertEqual(retrieved_log.calories, 1000)

    def test_sleep_log_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        sleep_log = SleepLog(
            user_id=user.id,
            start_time=datetime(2021, 1, 1, 22, 0, 0),
            end_time=datetime(2021, 1, 2, 6, 0, 0),
        )
        self.session.add(sleep_log)
        self.session.commit()

        retrieved_log = self.session.query(SleepLog).filter_by(user_id=user.id).one()
        self.assertEqual(retrieved_log.start_time, datetime(2021, 1, 1, 22, 0, 0))
        self.assertEqual(retrieved_log.end_time, datetime(2021, 1, 2, 6, 0, 0))

    def test_heart_rate_log_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        heart_rate_log = HeartRateLog(
            user_id=user.id,
            time_recorded=datetime(2021, 1, 1, 12, 0, 0),
            heart_rate=80,
        )
        self.session.add(heart_rate_log)
        self.session.commit()

        retrieved_log = (
            self.session.query(HeartRateLog).filter_by(user_id=user.id).one()
        )
        self.assertEqual(retrieved_log.heart_rate, 80)

    def test_health_metrics_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        health_metrics = HealthMetrics(
            user_id=user.id,
            date=date(2021, 1, 1),
            blood_pressure="120/80",
            bmi=22.0,
            resting_heart_rate=80,
            blood_oxygen_level=98.0,
            blood_sugar_level=100.0,
            daily_water_intake=2000,
        )
        self.session.add(health_metrics)
        self.session.commit()

        retrieved_log = (
            self.session.query(HealthMetrics).filter_by(user_id=user.id).one()
        )
        self.assertEqual(retrieved_log.blood_pressure, "120/80")
        self.assertEqual(retrieved_log.bmi, 22.0)
        self.assertEqual(retrieved_log.resting_heart_rate, 80)
        self.assertEqual(retrieved_log.blood_oxygen_level, 98.0)
        self.assertEqual(retrieved_log.blood_sugar_level, 100.0)
        self.assertEqual(retrieved_log.daily_water_intake, 2000)

    def test_user_fitness_goal_creation(self):
        user = self.create_user(username="testuser", age=25, email="test@mail.com")

        user_fitness_goal = UserFitnessGoal(
            user_id=user.id,
            goal_type_id=1,
            start_date=date(2021, 1, 1),
            end_date=date(2021, 12, 31),
            target={"weight": 70.0, "body_fat_percentage": 20.0},
        )
        self.session.add(user_fitness_goal)
        self.session.commit()

        retrieved_log = (
            self.session.query(UserFitnessGoal).filter_by(user_id=user.id).one()
        )
        self.assertEqual(retrieved_log.goal_type_id, 1)
        self.assertEqual(retrieved_log.start_date, date(2021, 1, 1))
        self.assertEqual(retrieved_log.end_date, date(2021, 12, 31))
        self.assertEqual(
            retrieved_log.target, {"weight": 70.0, "body_fat_percentage": 20.0}
        )


if __name__ == "__main__":
    unittest.main()
