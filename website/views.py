from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import City, Route


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])  
@login_required
def home():
    print("Home route accessed by:", current_user)
    cities = City.query.order_by(City.name).all()
    selected_route = None

    if request.method == 'POST':
        from_city_id = request.form.get('from_city')
        to_city_id = request.form.get('to_city')

        selected_route = Route.query.filter_by(
            from_city_id=from_city_id,
            to_city_id=to_city_id
        ).first()

    return render_template(
        'home.html',
        cities=cities,
        route=selected_route,
        user=current_user
    )