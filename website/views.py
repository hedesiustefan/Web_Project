from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import City, Route
from collections import deque, defaultdict
from datetime import datetime, timedelta
import heapq


views = Blueprint('views', __name__)

def parse_duration(duration_str):
    parts = duration_str.split()
    minutes = 0
    for part in parts:
        if part.endswith('h'):
            minutes += int(part[:-1]) * 60
        elif part.endswith('m'):
            minutes += int(part[:-1])
    return minutes

def is_connection_valid(arrival_time, next_departure_time, min_buffer=5):
    today = datetime.today().date()
    arr_dt = datetime.combine(today, arrival_time)
    dep_dt = datetime.combine(today, next_departure_time)
    return arr_dt + timedelta(minutes=min_buffer) <= dep_dt

def build_graph():
    routes = Route.query.all()
    graph = defaultdict(list)
    for route in routes:
        graph[route.from_city_id].append(route)
    return graph

def total_duration(route_list):
    today = datetime.today().date()
    start = datetime.combine(today, route_list[0].departure)
    end = datetime.combine(today, route_list[-1].arrival)
    return int((end - start).total_seconds() // 60)

def find_all_valid_paths(start_id, end_id, max_depth=4):
    graph = build_graph()
    all_paths = []
    queue = []

    for route in graph[start_id]:
        queue.append((route.to_city_id, route.arrival, [route]))

    while queue:
        current_city, last_arrival, path = queue.pop(0)

        if len(path) > max_depth:
            continue

        if current_city == end_id:
            duration = total_duration(path)
            all_paths.append((duration, path))
            continue

        for next_route in graph[current_city]:
            if next_route.to_city_id in [r.from_city_id for r in path]:
                continue  # prevent cycles

            if is_connection_valid(last_arrival, next_route.departure):
                new_path = path + [next_route]
                queue.append((next_route.to_city_id, next_route.arrival, new_path))

    return sorted(all_paths, key=lambda x: x[0])  # sort by duration

@views.route('/', methods=['GET', 'POST'])  
@login_required
def home():

    cities = City.query.all()
    selected_route = None
    all_possible_routes = []

    if request.method == 'POST':
        from_id = int(request.form.get('from_city'))
        to_id = int(request.form.get('to_city'))
        return redirect(url_for('views.home', from_id=from_id, to_id=to_id))

    from_id = request.args.get('from_id')
    to_id = request.args.get('to_id')
    route_index = request.args.get('route_index', default=0, type=int)

    if from_id and to_id:
        from_id = int(from_id)
        to_id = int(to_id)

        all_possible_routes = find_all_valid_paths(from_id, to_id)
        if route_index < len(all_possible_routes):
            selected_route = all_possible_routes[route_index][1]

    return render_template(
        "home.html",
        cities=cities,
        routes=selected_route,
        route_summaries=all_possible_routes,
        from_id=from_id,
        to_id=to_id,
        selected_index=route_index,
        user=current_user
    )
