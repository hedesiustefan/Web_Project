from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import City, Route
from collections import deque


views = Blueprint('views', __name__)

def find_route_path(from_id, to_id):
    visited = set()
    queue = deque()
    queue.append((from_id, []))  # (current_city_id, path_so_far)

    while queue:
        current_city_id, path = queue.popleft()

        if current_city_id in visited:
            continue
        visited.add(current_city_id)

        routes = Route.query.filter_by(from_city_id=current_city_id).all()

        for route in routes:
            new_path = path + [route]
            if route.to_city_id == to_id:
                return new_path
            queue.append((route.to_city_id, new_path))

    return None

@views.route('/', methods=['GET', 'POST'])  
@login_required
def home():
    
    cities = City.query.all()
    selected_path = None

    if request.method == 'POST':
        from_city_id = int(request.form.get('from_city'))
        to_city_id = int(request.form.get('to_city'))

        selected_path = find_route_path(from_city_id, to_city_id)

    return render_template(
        'home.html',
        cities=cities,
        path=selected_path,
        user=current_user
    )