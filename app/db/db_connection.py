import os

from db.models import Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(".env")

# Get the database connection string from an environment variable
database_url = os.environ.get("DATABASE_URL")

# Create an engine that connects to the specified database
engine = create_engine(database_url)

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
