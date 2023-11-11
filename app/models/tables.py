from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    DateTime,
    JSON,
    CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)

    workouts = relationship("WorkoutLog", back_populates="user")
    meals = relationship("NutritionLog", back_populates="user")
    sleep_records = relationship("SleepLog", back_populates="user")
    health_metrics = relationship("HealthMetrics", back_populates="user")
    height_logs = relationship("HeightLog", back_populates="user")
    weight_logs = relationship("WeightLog", back_populates="user")
    heart_rate_logs = relationship("HeartRateLog", back_populates="user")
    water_intake_logs = relationship("WaterIntakeLog", back_populates="user")
    fitness_goals = relationship("UserFitnessGoal", back_populates="user")


class HeightLog(Base):
    __tablename__ = "height_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    date_recorded = Column(Date)
    height = Column(Float, CheckConstraint("height > 0"))  # In centimeters (cm)

    user = relationship("User", back_populates="height_logs")


class WeightLog(Base):
    __tablename__ = "weight_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    date_recorded = Column(Date)
    weight = Column(Float, CheckConstraint("weight > 0"))  # In kilograms (kg)

    user = relationship("User", back_populates="weight_logs")


# Workout Log Table
class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    date = Column(Date)
    exercise_type = Column(String)
    duration = Column(Float)  # in minutes

    user = relationship("User", back_populates="workouts")
    heart_rate_logs = relationship("HeartRateLog", back_populates="workout_log")


class MealType(Base):
    __tablename__ = "meal_types"

    id = Column(Integer, primary_key=True)
    type_name = Column(String, unique=True)  # e.g., Breakfast, Lunch, etc.

    nutrition_logs = relationship("NutritionLog", back_populates="meal_type")


# Nutrition Log Table
class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    date = Column(Date)
    food = Column(String)
    calories = Column(Integer, CheckConstraint("calories > 0"))
    meal_type_id = Column(
        Integer, ForeignKey("meal_types.id"), index=True
    )  # Foreign Key

    user = relationship("User", back_populates="meals")
    meal_type = relationship("MealType", back_populates="nutrition_logs")


# Sleep Data Table
class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)

    user = relationship("User", back_populates="sleep_records")

    __table_args__ = (CheckConstraint("start_time < end_time"),)


# Health Metrics Table
class HealthMetrics(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    date = Column(Date, index=True)
    blood_pressure = Column(String)
    bmi = Column(Float)
    resting_heart_rate = Column(Integer, CheckConstraint("resting_heart_rate > 0"))
    blood_oxygen_level = Column(Float, CheckConstraint("blood_oxygen_level > 0"))
    blood_sugar_level = Column(Float, CheckConstraint("blood_sugar_level > 0"))
    daily_water_intake = Column(
        Integer, CheckConstraint("daily_water_intake > 0")
    )  # in ml

    user = relationship("User", back_populates="health_metrics")


class WaterIntakeLog(Base):
    __tablename__ = "water_intake_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    date = Column(Date)
    water_intake = Column(Integer, CheckConstraint("water_intake > 0"))  # in ml

    user = relationship("User", back_populates="water_intake_logs")


# Heart Rate Log Table
class HeartRateLog(Base):
    __tablename__ = "heart_rate_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    workout_log_id = Column(Integer, ForeignKey("workout_logs.id"), nullable=True)
    time_recorded = Column(DateTime)
    heart_rate = Column(Integer)  # Heart rate in beats per minute

    user = relationship("User", back_populates="heart_rate_logs")
    workout_log = relationship("WorkoutLog", back_populates="heart_rate_logs")


class FitnessGoalType(Base):
    __tablename__ = "fitness_goal_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    user_fitness_goals = relationship("UserFitnessGoal", back_populates="goal_type")


class UserFitnessGoal(Base):
    __tablename__ = "user_fitness_goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    goal_type_id = Column(Integer, ForeignKey("fitness_goal_types.id"))
    target = Column(JSON)  # e.g., {"weight": 70, "body_fat": 15}
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String)  # e.g., "Not Started", "In Progress", "Achieved"

    __table_args__ = (
        CheckConstraint("status IN ('Not Started', 'In Progress', 'Achieved')"),
        CheckConstraint("start_date <= end_date"),
    )

    user = relationship("User", back_populates="fitness_goals")
    goal_type = relationship("FitnessGoalType", back_populates="user_fitness_goals")
