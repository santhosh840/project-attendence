import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables if .env file exists
env_path = BASE_DIR / '.env'
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        pass

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-production-secret-key-987654321')
    
    # Database configuration
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'attendance_db')
    
    # Priority: DATABASE_URL env -> MySQL if configured -> SQLite fallback
    RAW_DB_URL = os.getenv('DATABASE_URL')
    if RAW_DB_URL:
        # Render/Heroku fix for postgresql:// -> postgresql+psycopg2:// if needed
        if RAW_DB_URL.startswith("postgres://"):
            RAW_DB_URL = RAW_DB_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = RAW_DB_URL
    elif DB_TYPE.lower() == 'mysql':
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        db_path = BASE_DIR / 'attendance.db'
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload paths
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    ENCODING_FOLDER = BASE_DIR / 'static' / 'encodings'
    UNKNOWN_FOLDER = BASE_DIR / 'static' / 'uploads' / 'unknown'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB Max Upload Limit

    # Email Settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')

    # Face Recognition Parameters
    FACE_MATCH_THRESHOLD = float(os.getenv('FACE_MATCH_THRESHOLD', 0.55))
    DUPLICATE_ATTENDANCE_COOLDOWN_MINUTES = int(os.getenv('DUPLICATE_ATTENDANCE_COOLDOWN_MINUTES', 60))
    LIVENESS_CHECK_ENABLED = os.getenv('LIVENESS_CHECK_ENABLED', 'True').lower() == 'true'
    LAPLACIAN_VARIANCE_THRESHOLD = float(os.getenv('LAPLACIAN_VARIANCE_THRESHOLD', 35.0))

    # Initial Admin Config
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@attendance.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': Config
}
