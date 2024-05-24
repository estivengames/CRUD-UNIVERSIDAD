
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

class Database:
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="login"
            )
            self.mycursor = self.mydb.cursor()
            print("Database connection successful.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_user(self, username, password):
        try:
            sql = "INSERT INTO Usuarios (nombre_usuario, contrasena) VALUES (%s, %s)"
            val = (username, password)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            return {"status": "success", "message": "User added successfully."}
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return {"status": "error", "message": str(err)}

    def get_all_users(self):
        try:
            self.mycursor.execute("SELECT * FROM Usuarios")
            return self.mycursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def delete_user(self, user_id):
        try:
            sql = "DELETE FROM Usuarios WHERE id = %s"
            val = (user_id,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            return {"status": "success", "message": "User deleted successfully."}
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return {"status": "error", "message": str(err)}

db = Database()

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    response = db.insert_user(username, password)
    return jsonify(response)

@app.route("/delete_user", methods=["POST"])
def delete_user():
    data = request.json
    user_id = data.get("user_id")
    response = db.delete_user(user_id)
    return jsonify(response)

@app.route("/refresh_list", methods=["GET"])
def refresh_list():
    users = db.get_all_users()
    return jsonify({"users": users})

if __name__ == "__main__":
    app.run()
