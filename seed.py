from website import create_app, db
from website.models import City, Route
from datetime import datetime

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


def route_exists(from_name, to_name, train_name):
    from_city = City.query.filter_by(name=from_name).first()
    to_city = City.query.filter_by(name=to_name).first()
    if not from_city or not to_city:
        return False
    return Route.query.filter_by(
        from_city_id=from_city.id,
        to_city_id=to_city.id,
        train_name=train_name
    ).first() is not None


# Create sample routes
def get_city_id(name):
    return City.query.filter_by(name=name).first().id

def to_time(t_str):
    return datetime.strptime(t_str, "%H:%M").time()

routes = [
    ("Berlin", "Hamburg", "ICE 808", "08:30", "10:15", "1h 45m"),
    ("Berlin", "Frankfurt", "ICE 1001", "07:00", "10:00", "3h"),
    ("Berlin", "Hamburg", "ICE 808", "08:00", "10:00", "2h"),
    ("Berlin", "Hamburg", "ICE 810", "09:00", "11:00", "2h"),
    ("Berlin", "Frankfurt", "ICE 500", "13:00", "16:00", "3h"),

    ("Frankfurt", "Munich", "ICE 622", "09:00", "12:30", "3h 30m"),
    ("Frankfurt", "Munich", "ICE 600", "10:45", "13:15", "2h 30m"),
    ("Frankfurt", "Munich", "ICE 601", "11:30", "14:00", "2h 30m"),

    ("Cologne", "Stuttgart", "IC 2310", "11:00", "13:45", "2h 45m"),

    ("Leipzig", "Dresden", "RE 50", "10:20", "11:30", "1h 10m"),

    
    ("Hamburg", "Munich", "ICE 1202", "13:00", "17:00", "4h"),
    ("Hamburg", "Munich", "ICE 900", "11:30", "16:00", "4h 30m"),
    ("Hamburg", "Munich", "ICE 901", "12:30", "17:00", "4h 30m"),

    ("Dresden", "Nuremberg", "RE 200", "15:00", "18:00", "3h"),

    ("Stuttgart", "Leipzig", "IC 3003", "12:00", "15:00", "3h"),

    ("Bremen", "Cologne", "RE 75", "06:30", "09:00", "2h 30m"),

    ("Munich", "Düsseldorf", "ICE 4004", "14:30", "17:30", "3h"),
    ("Munich", "Düsseldorf", "ICE 4005", "15:30", "18:30", "3h"),
    ("Munich", "Berlin", "ICE 4004", "10:30", "13:30", "3h"),
    ("Munich", "Frankfurt", "ICE 4005", "13:30", "16:30", "3h"),

]

for from_name, to_name, train, dep, arr, dur in routes:
    if not route_exists(from_name, to_name, train):
        from_id = get_city_id(from_name)
        to_id = get_city_id(to_name)
        new_route = Route(
            from_city_id=from_id,
            to_city_id=to_id,
            train_name=train,
            departure=to_time(dep),
            arrival=to_time(arr),
            duration=dur
        )
        db.session.add(new_route)

try:
    db.session.commit()
    print("New routes added (if not already present).")
except Exception as e:
    db.session.rollback()
    print(f"Error committing to DB: {e}")
