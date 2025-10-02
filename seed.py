#!/usr/bin/env python3
"""Script pour remplir la base de données HBnB avec des données de test"""
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place, PlaceImage
from app.models.amenity import Amenity
from app.models.reservation import Reservation
from app.models.review import Review

app = create_app()
app.app_context().push()

print("👉 Suppression des données existantes...")
db.session.query(Review).delete()
db.session.query(Reservation).delete()
db.session.query(PlaceImage).delete()
db.session.query(Place).delete()
db.session.query(Amenity).delete()
db.session.query(User).delete()
db.session.commit()

print("👉 Insertion des données de test...")

# Utilisateurs
users = [
    User(
        username="alice",
        email="alice@example.com",
        country="France",
        town="Paris",
        is_admin=False
    ),
    User(
        username="bob",
        email="bob@example.com",
        country="France",
        town="Lyon",
        is_admin=False
    ),
]

for user in users:
    user.set_password("password123")

db.session.add_all(users)
db.session.commit()

# Refresh pour récupérer les IDs générés
for user in users:
    db.session.refresh(user)

# Lieux
places = [
    Place(
        name="Appartement cosy",
        description="Un appartement charmant au centre-ville",
        price_by_night=70,
        country="France",
        town="Paris",
        owner_id=users[0].id
    ),
    Place(
        name="Maison avec piscine",
        description="Maison spacieuse avec piscine et jardin",
        price_by_night=150,
        country="France",
        town="Lyon",
        owner_id=users[1].id
    ),
]

db.session.add_all(places)
db.session.commit()

# Refresh pour récupérer les IDs des places
for place in places:
    db.session.refresh(place)

# Images de lieux
images = [
    PlaceImage(url="uploads/places/image1.jpg", place_id=places[0].id),
    PlaceImage(url="uploads/places/image2.jpg", place_id=places[1].id),
]
db.session.add_all(images)
db.session.commit()

# Équipements
amenities = [
    Amenity(name="Wi-Fi"),
    Amenity(name="Piscine"),
    Amenity(name="Climatisation"),
]
db.session.add_all(amenities)
db.session.commit()

# Associer les équipements aux lieux
places[0].amenities.append(amenities[0])  # Wi-Fi
places[0].amenities.append(amenities[2])  # Climatisation
places[1].amenities.append(amenities[1])  # Piscine
db.session.commit()

# Réservations
reservations = [
    Reservation(
        place_id=places[0].id,
        user_id=users[1].id,
        start_datetime=datetime.utcnow(),
        end_datetime=datetime.utcnow() + timedelta(days=3)
    ),
    Reservation(
        place_id=places[1].id,
        user_id=users[0].id,
        start_datetime=datetime.utcnow(),
        end_datetime=datetime.utcnow() + timedelta(days=7)
    ),
]
db.session.add_all(reservations)
db.session.commit()

# Avis
reviews = [
    Review(
        user_id=users[1].id,
        place_id=places[0].id,
        rating=5,
        comment="Super endroit, très confortable!"
    ),
    Review(
        user_id=users[0].id,
        place_id=places[1].id,
        rating=4,
        comment="Maison magnifique, belle piscine!"
    ),
]
db.session.add_all(reviews)
db.session.commit()

print("✅ Données de test insérées avec succès !")
