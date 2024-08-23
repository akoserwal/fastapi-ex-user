import logging
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


    @classmethod
    def first_or_fail(cls, name: str, db: Session):
        """
        Retrieve the first user by `name` or raise an exception if not found.
        Logs the operation details.
        """
        logger.info(f"Searching for user with name: {name}")

        user = db.query(cls).filter(cls.name == name).first()
        
        if user:
            logger.info(f"User found: {user}")
        else:
            logger.warning(f"User with name {name} not found")

        if not user:
            raise ValueError("User not found")

        return user
