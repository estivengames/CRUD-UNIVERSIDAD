import mysql.connector
from tkinter import *
import pytest
from tkinter import Listbox, Label, Entry, Button, Toplevel, END

class Database:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="login"
        )
        self.mycursor = self.mydb.cursor()

    def insert_user(self, username, password):
        sql = "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)"
        val = (username, password)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def get_all_users(self):
        self.mycursor.execute("SELECT * FROM usuarios")
        return self.mycursor.fetchall()

    def update_user(self, user_id, new_username, new_password):
        sql = "UPDATE usuarios SET nombre_usuario = %s, contrasena = %s WHERE id = %s"
        val = (new_username, new_password, user_id)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def delete_user(self, user_id):
        sql = "DELETE FROM usuarios WHERE id = %s"
        val = (user_id,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def clear_users(self):
        sql = "DELETE FROM usuarios"
        self.mycursor.execute(sql)
        self.mydb.commit()

class UserList:
    def __init__(self, root, db):
        self.root = root
        self.db = db

        self.user_list = Listbox(self.root, width=50)
        self.user_list.pack(pady=10)

        self.refresh_user_list()

    def refresh_user_list(self):
        self.user_list.delete(0, END)
        users = self.db.get_all_users()
        for user in users:
            self.user_list.insert(END, user)

class MainForm:
    def __init__(self, root, db):
        self.root = root
        self.db = db

        lbl_title = Label(self.root, text="Usuarios", font=("Arial", 20))
        lbl_title.pack(pady=10)

        self.user_list = UserList(self.root, self.db)

        btn_refresh = Button(self.root, text="Actualizar Lista", command=self.refresh_list)
        btn_refresh.pack(pady=5)

        btn_add_user = Button(self.root, text="Agregar Usuario", command=self.add_user)
        btn_add_user.pack(pady=5)

        btn_delete_user = Button(self.root, text="Eliminar Usuario", command=self.delete_user)
        btn_delete_user.pack(pady=5)

    def refresh_list(self):
        self.user_list.refresh_user_list()

    def add_user(self):
        add_window = Toplevel(self.root)
        add_window.title("Agregar Usuario")

        lbl_username = Label(add_window, text="Nombre de Usuario:")
        lbl_username.pack(pady=5)
        entry_username = Entry(add_window)
        entry_username.pack()

        lbl_password = Label(add_window, text="Contraseña:")
        lbl_password.pack(pady=5)
        entry_password = Entry(add_window, show="*")
        entry_password.pack()

        btn_add = Button(add_window, text="Agregar", command=lambda: self.add_user_to_db(add_window, entry_username.get(), entry_password.get()))
        btn_add.pack(pady=5)

    def add_user_to_db(self, add_window, username, password):
        self.db.insert_user(username, password)
        add_window.destroy()
        self.refresh_list()

    def delete_user(self):
        selected_user_index = self.user_list.user_list.curselection()
        if selected_user_index:
            user_id = self.user_list.user_list.get(selected_user_index)[0]
            self.db.delete_user(user_id)
            self.refresh_list()

def main():
    db = Database()
    root = Tk()
    main_form = MainForm(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()