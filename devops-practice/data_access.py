from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
import time

# Database connection configuration
DB_USER = 'root'
DB_PASSWORD = '123456789'
DB_HOST = 'sqlserver'
DB_NAME = 'three_tier_db'

# SQLAlchemy instance
db = SQLAlchemy()

# Function to create the database if it doesn't exist
def create_database_if_not_exists():
    connection_uri = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/'
    engine = create_engine(connection_uri)

    # Retry logic
    for _ in range(5):  # Retry up to 5 times
        try:
            with engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
                print(f"Database '{DB_NAME}' created or already exists.")
            break  # Exit loop if successful
        except Exception as e:
            print(f"Error connecting to database: {e}. Retrying...")
            time.sleep(5)

    engine.dispose()

# User model (represents the table structure)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

# Data access layer for interacting with the users table
class UserDataAccess:

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if user:
            return {'id': user.id, 'name': user.name, 'email': user.email}
        return None

    @staticmethod
    def create_user(name, email):
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}

    @staticmethod
    def update_user(user_id, name, email):
        user = User.query.get(user_id)
        if user:
            user.name = name
            user.email = email
            db.session.commit()
            return {'id': user.id, 'name': user.name, 'email': user.email}
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
