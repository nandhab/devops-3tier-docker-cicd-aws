from sqlalchemy import MetaData, Table, Column, Integer, String
from databases import Database

DATABASE_URL = "postgresql://postgres:postgres@db:5432/notesdb"

database = Database(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String)
)
