import json
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pymongo import MongoClient

postgres_url = URL.create(
    drivername="postgresql",
    username="user",  # change to your own database username
    host="localhost",
    database="parking",
)

postgres_engine = create_engine(postgres_url, echo=True)
postgres = postgres_engine.connect()

postgres.execute(text("DROP TABLE IF EXISTS hours"))

postgres.commit()