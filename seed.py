from werkzeug.security import generate_password_hash

from db import Database
from models import User, Trucks, Deliveries


def seed_database():
    admin = User(
        username="admin",
        password_hash=generate_password_hash("admin123"),
        role="admin"
    )

    guest1 = User(
        username="guest1",
        password_hash=generate_password_hash("guest123"),
        role="guest"
    )

    guest2 = User(
        username="guest2",
        password_hash=generate_password_hash("guest123"),
        role="guest"
    )

    trucks = [
        Trucks(name="Truck 1", registration_number="N001WB", status="available"),
        Trucks(name="Truck 2", registration_number="N002WB", status="available"),
        Trucks(name="Truck 3", registration_number="N003WB", status="in transit"),
        Trucks(name="Truck 4", registration_number="N004WB", status="maintenance"),
        Trucks(name="Truck 5", registration_number="N005WB", status="available"),
    ]

    Database.session.add_all([admin, guest1, guest2])
    Database.session.add_all(trucks)
    Database.session.commit()

    deliveries = [
        Deliveries(origin="Walvis Bay", destination="Windhoek", weight=1200, assigned_truck_id=trucks[0].id, status="pending"),
        Deliveries(origin="Windhoek", destination="Oshakati", weight=850, assigned_truck_id=trucks[1].id, status="pending"),
        Deliveries(origin="Walvis Bay", destination="Swakopmund", weight=500, assigned_truck_id=trucks[2].id, status="in progress"),
        Deliveries(origin="Windhoek", destination="Rundu", weight=1500, assigned_truck_id=trucks[3].id, status="pending"),
        Deliveries(origin="Rundu", destination="Katima Mulilo", weight=900, assigned_truck_id=trucks[4].id, status="completed"),
        Deliveries(origin="Walvis Bay", destination="Gaborone", weight=2100, assigned_truck_id=trucks[0].id, status="pending"),
        Deliveries(origin="Windhoek", destination="Lusaka", weight=1800, assigned_truck_id=trucks[1].id, status="in progress"),
        Deliveries(origin="Oshakati", destination="Ondangwa", weight=650, assigned_truck_id=trucks[2].id, status="completed"),
        Deliveries(origin="Swakopmund", destination="Walvis Bay", weight=400, assigned_truck_id=trucks[3].id, status="pending"),
        Deliveries(origin="Windhoek", destination="Cape Town", weight=2500, assigned_truck_id=trucks[4].id, status="pending"),
    ]

    Database.session.add_all(deliveries)
    Database.session.commit()