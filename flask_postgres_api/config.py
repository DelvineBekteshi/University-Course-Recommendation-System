import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user_admin:password123@localhost:5432/university_recommendations"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0