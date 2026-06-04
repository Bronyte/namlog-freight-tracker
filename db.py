from flask_sqlalchemy import SQLAlchemy

Database = SQLAlchemy()

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def get_database(self):
        return Database


def test_database_singleton():
    manager_one = DatabaseManager()
    manager_two = DatabaseManager()

    print("Testing DatabaseManager Singleton...")
    print("Manager instance 1 ID:", id(manager_one))
    print("Manager instance 2 ID:", id(manager_two))

    if manager_one is manager_two:
        print("PASS: DatabaseManager is a Singleton.")
    else:
        print("FAIL: DatabaseManager is not a Singleton.")
    


