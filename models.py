from db import Database

class User(Database.Model):
    __tablename__ = "users"

    id = Database.Column(Database.Integer, primary_key=True)
    username = Database.Column(Database.String(80), unique=True, nullable=False)
    password_hash = Database.Column(Database.String(255), nullable=False)
    role = Database.Column(Database.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }


class Trucks(Database.Model):

    __tablename__ = 'trucks'

    id = Database.Column(Database.Integer, primary_key=True)
    name = Database.Column(Database.String(80), nullable=False)
    registration_number = Database.Column(Database.String(80), unique=True, nullable=False)
    status = Database.Column(Database.String(80), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_number": self.registration_number,
            "status": self.status
        }

class Deliveries(Database.Model):
    __tablename__ = 'deliveries'

    id = Database.Column(Database.Integer, primary_key=True)
    origin = Database.Column(Database.String(80), nullable=False)
    destination = Database.Column(Database.String(80), nullable=False)
    weight = Database.Column(Database.Integer, nullable=False)
    assigned_truck_id = Database.Column(Database.Integer, Database.ForeignKey('trucks.id'), nullable=False)
    status = Database.Column(Database.String(80), nullable=False)

    truck = Database.relationship('Trucks', backref=Database.backref('deliveries', lazy=True), foreign_keys=[assigned_truck_id])

    def to_dict(self):
        return {
            "id": self.id,
            "registration_number": self.registration_number,
            "origin": self.origin,
            "destination": self.destination,
            "weight": self.weight,
            "truck": self.assigned_truck_id,
            "status": self.status
        }