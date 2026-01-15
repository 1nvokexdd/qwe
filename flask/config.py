import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL connection from Django project
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'disco-db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    @property
    def DATABASE_URI(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
