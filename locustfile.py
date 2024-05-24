from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 3)

    @task
    def add_user(self):
        username = "test_user"
        password = "password123"
        self.client.post("/add_user", json={"username": username, "password": password})

    @task
    def delete_user(self):
        self.client.post("/delete_user", json={"user_id": 1})

    @task
    def refresh_list(self):
        self.client.get("/refresh_list")