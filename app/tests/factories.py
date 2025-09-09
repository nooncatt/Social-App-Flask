from uuid import uuid4
from faker import Faker
import random

fake = Faker("ru_RU")


def create_user_payload():
    return {
        "first_name": "Vasya" + str(uuid4()),
        "last_name": "Pypkin" + str(uuid4()),
        "email": f"vasya{uuid4()}@gmail.com",
    }


def create_post_payload(author_id):
    return {
        "author_id": author_id,
        "text": fake.sentence(),
    }


def create_react_payload(user_id):
    return {
        "user_id": user_id,
        "reaction": random.choice(
            ["heart", "like", "dislike", "boom", "angry", "haha", "wow"]
        ),
    }
