import pytest
from test_unitari import Database  

@pytest.fixture
def db():
    db = Database()
    db.clear_users() 
    return db

def test_insert_user(db):
    db.insert_user("test_user", "password123")
    users = db.get_all_users()
    assert any(user[1] == "test_user" for user in users)

def test_update_user(db):
    db.insert_user("old_user", "password123")
    users = db.get_all_users()
    user_id = users[0][0]

    db.update_user(user_id, "new_user", "new_password")
    users = db.get_all_users()
    updated_user = next(user for user in users if user[0] == user_id)

    assert updated_user[1] == "new_user"
    assert updated_user[2] == "new_password"

def test_delete_user(db):
    db.insert_user("delete_user", "password123")
    users = db.get_all_users()
    user_id = users[0][0]

    db.delete_user(user_id)
    users_after_deletion = db.get_all_users()

    assert not any(user[0] == user_id for user in users_after_deletion)

def test_get_all_users(db):
    db.insert_user("user1", "password123")
    db.insert_user("user2", "password456")
    users = db.get_all_users()

    assert len(users) == 2
    assert users[0][1] == "user1"
    assert users[1][1] == "user2"

def test_clear_users(db):
    db.insert_user("user1", "password123")
    db.clear_users()
    users = db.get_all_users()

    assert len(users) == 0
