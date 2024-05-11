from django.test import TestCase
from django.urls import reverse
from apps.route.models import Route, Boat
from apps.route.utils import find_routes_with_weekday


class ViewRouteTestCase(TestCase):
    def setUp(self):
        # Create boats
        boat_1 = Boat.objects.create(
            name='Boat 1',
            capacity='30',
        )

        boat_2 = Boat.objects.create(
            name='Boat 2',
            capacity='50',
        )

        # Create routes
        Route.objects.create(
            origin='A',
            destination='B',
            weekday='Monday',
            boat=boat_1,
            value='100.00',
        )

        Route.objects.create(
            origin='B',
            destination='C',
            weekday='Monday',
            boat=boat_2,
            value='100.00',
        )

        Route.objects.create(
            origin='A',
            destination='C',
            weekday='Monday',
            boat=boat_1,
            value='100.00',
        )

        Route.objects.create(
            origin='A',
            destination='B',
            weekday='Monday',
            boat=boat_2,
            value='100.00',
        )

        Route.objects.create(
            origin='B',
            destination='C',
            weekday='Monday',
            boat=boat_1,
            value='100.00',
        )

    def find_routes_with_weekday(self):
        found_routes = find_routes_with_weekday('A', 'C', 'Monday')
        print(found_routes)
        self.assertEqual(len(found_routes), 3)
        self.assertEqual(found_routes[0], [1, 2])
        self.assertEqual(found_routes[1], [1, 3])
        self.assertEqual(found_routes[2], [4, 2])

