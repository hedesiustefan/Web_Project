from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import City, Route
from collections import deque, defaultdict
from datetime import datetime, timedelta
import heapq


views = Blueprint('views', __name__)

def parse_duration(duration_str):
    # Expects format like "1h 45m"
    parts = duration_str.split()
    minutes = 0
    for part in parts:
        if part.endswith('h'):
            minutes += int(part[:-1]) * 60
        elif part.endswith('m'):
            minutes += int(part[:-1])
    return minutes

def is_connection_valid(arrival_time, next_departure_time, min_buffer=5):
    # Convert times to datetime for easy comparison
    today = datetime.today().date()
    arr_dt = datetime.combine(today, arrival_time)
    dep_dt = datetime.combine(today, next_departure_time)

    # Allow minimum buffer (e.g., 5 minutes between trains)
    return arr_dt + timedelta(minutes=min_buffer) <= dep_dt

def build_graph():
    routes = Route.query.all()
    graph = defaultdict(list)

    for route in routes:
        graph[route.from_city_id].append(route)
    
    return graph

def find_fastest_path(start_id, end_id):
    graph = build_graph()
    heap = []  # (total_time_in_minutes, current_city_id, arrival_time, path_taken)

    # Start with all routes from start city
    for route in graph[start_id]:
        heapq.heappush(heap, (
            parse_duration(route.duration),
            route.to_city_id,
            route.arrival,
            [route]
        ))

    visited = dict()  # city_id -> earliest arrival

    while heap:
        total_minutes, current_city, last_arrival, path = heapq.heappop(heap)

        if current_city == end_id:
            return path

        if current_city in visited:
            if visited[current_city] <= last_arrival:
                continue  # Skip if we've already arrived earlier
        visited[current_city] = last_arrival

        for next_route in graph[current_city]:
            if is_connection_valid(last_arrival, next_route.departure):
                new_duration = total_minutes + parse_duration(next_route.duration)
                new_path = path + [next_route]
                heapq.heappush(heap, (
                    new_duration,
                    next_route.to_city_id,
                    next_route.arrival,
                    new_path
                ))

    return None

@views.route('/', methods=['GET', 'POST'])  
@login_required
def home():

    cities = City.query.all()
    selected_routes = None

    if request.method == 'POST':
        from_city_id = int(request.form.get('from_city'))
        to_city_id = int(request.form.get('to_city'))

        selected_routes = find_fastest_path(from_city_id, to_city_id)

    return render_template(
        "home.html",
        cities=cities,
        routes=selected_routes,
        user=current_user
    )