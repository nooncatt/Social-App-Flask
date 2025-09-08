import pytest
from app import app, USERS, POSTS

@pytest.fixture(autouse=True)
def isolate_state():
    app.config.update(TESTING=True)
    USERS.clear()
    POSTS.clear()
    yield
    USERS.clear()
    POSTS.clear()

@pytest.fixture
def client():
    with app.test_client() as c:
        yield c
