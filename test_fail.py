import pytest
import mysql.connector
import tkinter as tk
from tkinter import Listbox, Label, Entry, Button, Toplevel, END

class Database:
    def __init__(self, db_name):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database=db_name
            )
            self.mycursor = self.mydb.cursor()
            print("Database connection successful.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_user(self, username, password):
        try:
            sql = "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)"
            val = (username, password)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            print(f"User {username} inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_all_users(self):
        try:
            self.mycursor.execute("SELECT * FROM usuarios")
            result = self.mycursor.fetchall()
            print("Users fetched successfully: ", result)
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def clear_users(self):
        try:
            sql = "DELETE FROM usuarios"
            self.mycursor.execute(sql)
            self.mydb.commit()
            print("All users cleared successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_user(self, user_id, new_username, new_password):
        try:
            sql = "UPDATE usuarios SET nombre_usuario = %s, contrasena = %s WHERE id = %s"
            val = (new_username, new_password, user_id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            print(f"User {user_id} updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_user(self, user_id):
        try:
            sql = "DELETE FROM usuarios WHERE id = %s"
            val = (user_id,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            print(f"User {user_id} deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

# Prueba unitaria para verificar la inserción de usuarios en la base de datos
def test_insert_user():
    db = Database("login")
    db.clear_users()  # Limpiar la base de datos antes de ejecutar la prueba

    db.insert_user("integration_user", "password123")

    users = db.get_all_users()
    assert any(user[1] == "integration_user" for user in users)

    db.clear_users()  # Limpiar la base de datos después de la prueba

# Pruebas de regresión
def test_update_user():
    db = Database("login")
    db.clear_users()

    db.insert_user("old_username", "old_password")
    users = db.get_all_users()
    user_id = users[0][0]  # Obtener el ID del primer usuario

    db.update_user(user_id, "new_username", "new_password")
    users = db.get_all_users()
    updated_user = users[0]

    assert updated_user[1] == "new_username"
    assert updated_user[2] == "new_password"

    db.clear_users()

def test_delete_user():
    db = Database("login")
    db.clear_users()

    db.insert_user("delete_me", "password123")
    users = db.get_all_users()
    user_id = users[0][0]  # Obtener el ID del primer usuario

    db.delete_user(user_id)
    users_after_deletion = db.get_all_users()

    assert not any(user[1] == "delete_me" for user in users_after_deletion)

    db.clear_users()

@pytest.mark.parametrize("input_data, expected", [(1, 2), (3, 4)])
def test_example(input_data, expected):
    assert input_data + 1 == expected

@pytest.mark.xfail
def test_example_that_should_fail():
    assert 1 == 2
