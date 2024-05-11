from collections import deque
from django.db.models import Q

from apps.route.models import Route

def find_routes_with_weekday(origin, destination, weekday):
    queue = deque([(origin, [])])
    visited = set()
    found_routes = []

    while queue:
        current_point, current_path = queue.popleft()

        if current_point == destination:
            # Add the route ID to the found path
            path_with_ids = [route.id for route in current_path]
            found_routes.append(path_with_ids)
            continue

        if current_point not in visited:
            visited.add(current_point)

            # Search for routes connected to the current point with matching weekday
            connected_routes = Route.objects.filter(
                Q(origin=current_point) | Q(destination=current_point),
                weekday=weekday
            )

            for route in connected_routes:
                next_point = route.origin if route.destination == current_point else route.destination
                queue.append((next_point, current_path + [route]))

    return found_routes