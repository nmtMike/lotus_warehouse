from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

url_object = URL.create(
    "postgresql",
    username="lotus",
    password="lotus",
    host="localhost",
    port="5433",
    database="lotusdb")

engine = create_engine(url_object)
session = Session(engine)

