from app.models.tables import (
    User,
    WeightLog,
    WorkoutLog,
    NutritionLog,
    SleepLog,
    HealthMetrics,
    HeartRateLog,
    WaterIntakeLog,
    UserFitnessGoal,
)
from sqlalchemy import func


def get_user_total_workout_duration(session, user_id, start_date, end_date):
    """Get the total amount of time spent working out by a user between two dates

    Args:
        session (db session): SQLAlchemy database session
        user_id (int): ID of the user
        start_date (date): Start date of the time period
        end_date (date): End date of the time period

    Returns:
        float: Total workout duration in minutes
    """
    total_duration = (
        session.query(func.sum(WorkoutLog.duration))
        .filter(WorkoutLog.user_id == user_id)
        .filter(WorkoutLog.date.between(start_date, end_date))
        .scalar()
    )
    return total_duration


def get_user_avg_daily_caloric_intake(session, user_id):
    """Calculate the average daily caloric intake for a user.

    Args:
        session (db session): SQLAlchemy database session
        user_id (int): ID of the user

    Returns:
        float: Average daily caloric intake
    """
    avg_calories = (
        session.query(func.avg(NutritionLog.calories))
        .filter(NutritionLog.user_id == user_id)
        .scalar()
    )
    return avg_calories


def get_user_avg_sleep_duration(session, user_id):
    """Calculate the average sleep duration for a user.

    Args:
        session (db session): SQLAlchemy database session
        user_id (int): ID of the user

    Returns:
        float: Average sleep duration in hours
    """
    avg_sleep_duration = (
        session.query(
            func.avg(
                func.julianday(SleepLog.end_time) - func.julianday(SleepLog.start_time)
            )
            * 24
        )
        .filter(SleepLog.user_id == user_id)
        .scalar()
    )
    return avg_sleep_duration


def get_user_weight_records(session, user_id):
    """Retrieve weight records over time for a user.

    Args:
        session (db session): SQLAlchemy database session
        user_id (int): ID of the user

    Returns:
        list of tuples: List containing (date_recorded, weight)
    """
    weight_records = (
        session.query(WeightLog.date_recorded, WeightLog.weight)
        .filter(WeightLog.user_id == user_id)
        .order_by(WeightLog.date_recorded.asc())
        .all()
    )
    return weight_records


def get_users_not_meeting_sleep_goals(session, sleep_hours_goal):
    """Find users who are not meeting their sleep goals.

    Args:
        session (db session): SQLAlchemy database session
        sleep_hours_goal (float): Target sleep hours per day

    Returns:
        list: List of usernames not meeting sleep goals
    """
    users_not_meeting_sleep_goal = (
        session.query(User.username)
        .join(SleepLog)
        .join(UserFitnessGoal)
        .filter(UserFitnessGoal.target.contains("sleep"))
        .group_by(User.id)
        .having(
            func.avg(
                func.julianday(SleepLog.end_time) - func.julianday(SleepLog.start_time)
            )
            < sleep_hours_goal / 24
        )
        .all()
    )
    return [user.username for user in users_not_meeting_sleep_goal]


def get_user_daily_water_intake(session, user_id, specific_date):
    """Calculate the total water intake for a user on a specific date.

    Args:
        session (db session): SQLAlchemy database session
        user_id (int): ID of the user
        specific_date (date): The specific date for which water intake is calculated

    Returns:
        int: Total water intake in milliliters
    """
    total_water_intake = (
        session.query(func.sum(WaterIntakeLog.water_intake))
        .filter(WaterIntakeLog.user_id == user_id)
        .filter(WaterIntakeLog.date == specific_date)
        .scalar()
    )
    return total_water_intake or 0


def get_user_recent_blood_pressure(session, user_id, number_of_records=5):
    """Retrieve the most recent blood pressure readings for a user.

    Args:
        session (db session): SQLAlchemy database session
        user_id (int): ID of the user
        number_of_records (int): Number of recent records to retrieve

    Returns:
        list of tuples: List containing (date, blood_pressure)
    """
    recent_bp_readings = (
        session.query(HealthMetrics.date, HealthMetrics.blood_pressure)
        .filter(HealthMetrics.user_id == user_id)
        .order_by(HealthMetrics.date.desc())
        .limit(number_of_records)
        .all()
    )
    return recent_bp_readings


def get_user_avg_heart_rate_during_workouts(session, user_id):
    """Calculate the average heart rate during workouts for a user.

    Args:
        session (db session): SQLAlchemy database session
        user_id (int): ID of the user

    Returns:
        float: Average heart rate during workouts
    """
    avg_heart_rate = (
        session.query(func.avg(HeartRateLog.heart_rate))
        .join(WorkoutLog, HeartRateLog.workout_log_id == WorkoutLog.id)
        .filter(WorkoutLog.user_id == user_id)
        .scalar()
    )
    return avg_heart_rate or 0


def run_queries(session):
    """Run all the queries and print the results"""
    print(
        "Total workout duration for user 1:",
        get_user_total_workout_duration(session, 1, "2020-01-01", "2020-12-31"),
    )
    print(
        "Average daily caloric intake for user 1:",
        get_user_avg_daily_caloric_intake(session, 1),
    )
    print("Average sleep duration for user 1:", get_user_avg_sleep_duration(session, 1))
    print("Weight records for user 1:", get_user_weight_records(session, 1))
    print(
        "Users not meeting sleep goals:", get_users_not_meeting_sleep_goals(session, 8)
    )
    print(
        "Water intake for user 1 on 2020-01-01:",
        get_user_daily_water_intake(session, 1, "2020-01-01"),
    )
    print(
        "Recent blood pressure readings for user 1:",
        get_user_recent_blood_pressure(session, 1),
    )
    print(
        "Average heart rate during workouts for user 1:",
        get_user_avg_heart_rate_during_workouts(session, 1),
    )
