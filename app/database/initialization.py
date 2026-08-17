"""
app/database/initialization.py

This will create the database tables and so on
so here first i will import all the tables first
"""

from sqlmodel import SQLModel


from .engine import engine

# This models module is where all the class of table will be defined
from .models import *


def create_db_and_tables():
    SQLModel.metadata.create_all(
        bind=engine,
    )
