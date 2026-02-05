from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Project(Base):
    """Database model for storing project details."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    total_cost = Column(Float, nullable=False)


DATABASE_URL = "sqlite:///data/databases/user_projects.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
