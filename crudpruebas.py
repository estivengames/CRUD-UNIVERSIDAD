import pytest
from tkinter import Tk, Label, Entry, Button

class MainForm:
    def __init__(self, master=None, db=None):
        self.master = master if master else Tk()
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        # Aquí se crean los widgets de la interfaz de usuario
        self.label = Label(self.master, text="Nombre de usuario:")
        self.label.pack()
        
        self.entry = Entry(self.master)
        self.entry.pack()

        self.button = Button(self.master, text="Agregar usuario", command=self.add_user)
        self.button.pack()

    def add_user(self):
        # Aquí se implementa la lógica para agregar un usuario a la base de datos
        if self.db:
            username = self.entry.get()
            self.db.add_user(username)
            
# Clase simulada para la base de datos en pruebas
class MockDB:
    def __init__(self):
        self.users = []

    def add_user(self, username):
        self.users.append(username)

@pytest.fixture
def db():
    return MockDB()

@pytest.fixture
def app(db):
    return MainForm(db=db)

def test_add_user(app, db):
    initial_users = db.users
    app.add_user()
    new_users = db.users
    assert len(new_users) == len(initial_users) + 1

# Ejecutar las pruebas
if __name__ == "__main__":
    pytest.main([__file__])