# __init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.tables import Base

engine = create_engine("sqlite:///health_fitness_app.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
