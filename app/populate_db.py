# populate_db.py
from faker import Faker
import random
import json
from app.models.tables import (
    User,
    HeightLog,
    WeightLog,
    WorkoutLog,
    NutritionLog,
    SleepLog,
    HealthMetrics,
    HeartRateLog,
    MealType,
    WaterIntakeLog,
    FitnessGoalType,
    UserFitnessGoal,
)
from datetime import timedelta

fake = Faker()

FOOD_ITEMS = [
    "Pasta",
    "Rice",
    "Chicken Salad",
    "Vegetable Stir Fry",
    "Beef Stew",
    "Grilled Cheese Sandwich",
    "Tofu Curry",
]

FITNESS_GOAL_TYPES = [
    {"name": "Lose Weight", "description": "Lose a certain amount of weight"},
    {"name": "Gain Weight", "description": "Gain a certain amount of weight"},
    {"name": "Build Muscle", "description": "Build muscle mass"},
    {"name": "Improve Cardio", "description": "Improve cardiovascular health"},
]


def create_fake_user():
    return User(
        username=fake.user_name(), age=random.randint(18, 80), email=fake.email()
    )


def create_fake_height_log(user):
    return HeightLog(
        user=user,
        date_recorded=fake.date_between(start_date="-10y", end_date="today"),
        height=random.uniform(150.0, 200.0),  # Height in cm
    )


def create_fake_weight_log(user):
    return WeightLog(
        user=user,
        date_recorded=fake.date_between(start_date="-10y", end_date="today"),
        weight=random.uniform(50.0, 100.0),  # Weight in kg
    )


def create_fake_workout_log(user):
    return WorkoutLog(
        user=user,
        date=fake.date_between(start_date="-10y", end_date="today"),
        exercise_type=random.choice(["Running", "Swimming", "Cycling", "Yoga"]),
        duration=random.uniform(30.0, 120.0),  # Duration in minutes
    )


def create_fake_water_intake_log(user):
    return WaterIntakeLog(
        user=user,
        date=fake.date_between(start_date="-10y", end_date="today"),
        water_intake=random.randint(0, 5000),  # Water intake in ml
    )


def create_fake_nutrition_log(user, meal_type_id):
    return NutritionLog(
        user=user,
        date=fake.date_between(start_date="-10y", end_date="today"),
        food=random.choice(FOOD_ITEMS),
        calories=random.randint(100, 1000),
        meal_type_id=meal_type_id,
    )


def create_fake_sleep_log(user):
    start_time = fake.date_time_between(start_date="-10y", end_date="now")
    end_time = start_time + timedelta(hours=random.randint(6, 10))
    return SleepLog(user=user, start_time=start_time, end_time=end_time)


def create_fake_health_metrics(user):
    return HealthMetrics(
        user=user,
        date=fake.date_between(start_date="-10y", end_date="today"),
        blood_pressure=f"{random.randint(70, 120)}/{random.randint(40, 80)}",
        resting_heart_rate=random.randint(50, 80),
        blood_oxygen_level=random.randint(95, 100),
        blood_sugar_level=random.randint(70, 120),
    )


def create_fake_heart_rate_log(user, workout_log=None):
    return HeartRateLog(
        user=user,
        workout_log=workout_log,
        time_recorded=fake.date_time_between(start_date="-10y", end_date="now"),
        heart_rate=random.randint(60, 180),  # Heart rate in bpm
    )


def create_fake_fitness_goal(user, goal_type_id):
    # Generate a fake target JSON containing relevant user metrics
    target = {
        "weight": random.uniform(
            50, 100
        ),  # Example: Random weight between 50 and 100 kg
        "body_fat_percentage": random.uniform(
            10, 30
        ),  # Example: Random body fat percentage between 10% and 30%
        # Add more relevant metrics as needed
    }

    start_date = fake.date_between(start_date="-10y", end_date="today")
    end_date = fake.date_between(start_date=start_date, end_date="today")

    return UserFitnessGoal(
        user=user,
        goal_type_id=goal_type_id,
        target=json.dumps(target),  # Convert the dictionary to a JSON string
        start_date=start_date,
        end_date=end_date,
        status=random.choice(["Not Started", "In Progress", "Achieved"]),
    )


def populate_meal_types(session):
    # Check if the MealType table is already populated
    if session.query(MealType).count() == 0:
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snack", "Other"]
        for mt in meal_types:
            session.add(MealType(type_name=mt))
        session.commit()
        print("Meal types populated.")
    else:
        print("Meal types already exist.")


def populate_fitness_goal_types(session):
    # Check if the FitnessGoalType table is already populated
    if session.query(FitnessGoalType).count() == 0:
        for goal_type in FITNESS_GOAL_TYPES:
            session.add(FitnessGoalType(**goal_type))
        session.commit()
        print("Fitness goal types populated.")
    else:
        print("Fitness goal types already exist.")


def populate_user_fitness_goals(session, user):
    # Check if the UserFitnessGoal table is already populated
    if session.query(UserFitnessGoal).filter_by(user_id=user.id).count() == 0:
        possible_goal_types = session.query(FitnessGoalType).all()

        # Randomly select a few goal types
        num_goal_types = random.randint(1, len(possible_goal_types))
        goal_types = random.sample(possible_goal_types, num_goal_types)

        # Create a fitness goal for each goal type
        for goal_type in goal_types:
            session.add(create_fake_fitness_goal(user, goal_type.id))
        session.commit()
        print(f"Fitness goals populated for user {user.id}.")
    else:
        print(f"Fitness goals already exist for user {user.id}.")


def populate_database(session, num_users=10, num_logs_per_user=5):
    # First, ensure MealType table is populated
    populate_meal_types(session)
    populate_fitness_goal_types(session)

    # Fetch meal type IDs
    meal_type_ids = [mt.id for mt in session.query(MealType).all()]

    for _ in range(num_users):
        user = create_fake_user()
        session.add(user)
        session.flush()  # This assigns an ID to the user

        # Populate fitness goals for the user
        populate_user_fitness_goals(session, user)
        for _ in range(num_logs_per_user):
            session.add(create_fake_height_log(user))
            session.add(create_fake_weight_log(user))
            workout_log = create_fake_workout_log(user)
            session.add(workout_log)

            meal_type_id = random.choice(meal_type_ids)
            session.add(create_fake_nutrition_log(user, meal_type_id))

            session.add(create_fake_sleep_log(user))
            session.add(create_fake_health_metrics(user))
            session.add(create_fake_heart_rate_log(user, workout_log))
            session.add(create_fake_water_intake_log(user))

    session.commit()
    print(
        f"Added fake data for {num_users} users and their associated logs to the database."
    )
