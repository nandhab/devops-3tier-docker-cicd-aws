from databases import Database
from sqlalchemy import Table, Column, Integer, String, DateTime, JSON, MetaData


DATABASE_URL = "postgresql://postgres:postgres@db:5432/notesdb"

database = Database(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String, nullable=False),
    Column("tags", JSON, nullable=True),  # Stores list of tags as JSON
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
)