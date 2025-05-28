from website import create_app, db
from website.models import City, Route

app = create_app()
app.app_context().push()

cities = [
    "Berlin", "Hamburg", "Munich", "Frankfurt", "Cologne",
    "Stuttgart", "Düsseldorf", "Leipzig", "Hanover", "Nuremberg",
    "Dresden", "Bremen", "Essen", "Dortmund", "Mannheim",
    "Karlsruhe", "Freiburg", "Mainz", "Koblenz", "Aachen"
]

# Create cities
city_objs = []
for city_name in cities:
    existing = City.query.filter_by(name=city_name).first()
    if not existing:
        city_obj = City(name=city_name)
        db.session.add(city_obj)
        city_objs.append(city_obj)

db.session.commit()

# Create sample routes
def get_city_id(name):
    return City.query.filter_by(name=name).first().id

routes = [
    ("Berlin", "Hamburg", "ICE 808", "08:30", "10:15", "1h 45m"),
    ("Frankfurt", "Munich", "ICE 622", "09:00", "12:30", "3h 30m"),
    ("Cologne", "Stuttgart", "IC 2310", "11:00", "13:45", "2h 45m"),
    ("Leipzig", "Dresden", "RE 50", "10:20", "11:30", "1h 10m"),
]

for from_name, to_name, train, dep, arr, dur in routes:
    from_id = get_city_id(from_name)
    to_id = get_city_id(to_name)
    db.session.add(Route(
        from_city_id=from_id,
        to_city_id=to_id,
        train_name=train,
        departure=dep,
        arrival=arr,
        duration=dur
    ))

db.session.commit()
print("Database seeded.")
