# main.py
from app import Session
from app.populate_db import populate_database
from app.models.tables import User
from app.queries import run_queries


def main():
    session = Session()

    # Populate the database with fake data
    if not session.query(User).all():
        try:
            populate_database(session, num_users=20, num_logs_per_user=10)
        finally:
            session.close()

    # Run the queries
    run_queries(session)


if __name__ == "__main__":
    main()
