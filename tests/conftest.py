import pytest
from app.database import db


@pytest.fixture(autouse=True)
def clean_db():
    db.clear()
    yield
    db.clear()