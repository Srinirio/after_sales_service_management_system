from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    PROJECT_NAME: str = "After Sales Service Management System"
    API_V1_STR: str = "/Service_Management_System"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DESCRIPTION: str = "Service Management System"
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:@localhost/service_management_system"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    
settings = Settings()
    