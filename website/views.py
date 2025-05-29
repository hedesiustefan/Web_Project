from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import City, Route
from collections import deque


views = Blueprint('views', __name__)

def find_route_path(from_id, to_id, all_routes):
    graph = {}

    # Build adjacency list
    for route in all_routes:
        graph.setdefault(route.from_city_id, []).append(route)

    visited = set()
    queue = deque([[[] , from_id]])  # path_so_far, current_city

    while queue:
        path, city = queue.popleft()
        if city == to_id:
            return path  # full path of Route objects

        if city in visited:
            continue
        visited.add(city)

        for route in graph.get(city, []):
            if route.to_city_id not in visited:
                queue.append([path + [route], route.to_city_id])

    return None  # No path found


@views.route('/', methods=['GET', 'POST'])  
@login_required
def home():
    #print("Home route accessed by:", current_user)
    selected_routes = None
    cities = City.query.all()
    
    if request.method == 'POST':
        from_city_id = int(request.form.get('from_city'))
        to_city_id = int(request.form.get('to_city'))
        all_routes = Route.query.all()
        selected_routes = find_route_path(from_city_id, to_city_id, all_routes)

    return render_template(
        'home.html',
        cities=cities,
        route_path=selected_routes,
        user=current_user
    )