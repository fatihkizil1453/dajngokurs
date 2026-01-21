from django.test import TestCase
from .utils import estimate_price
from .forms import EstimateForm


class EstimatorUtilsTests(TestCase):
    def test_basic_estimate(self):
        price = estimate_price(100, 3, 2, 10)
        # Sanity checks: number should be positive and within a reasonable range
        # (With the higher scaling in this demo, values are expected to be in millions)
        self.assertTrue(price > 0)
        self.assertTrue(price < 10000000)

    def test_multiplier_clamp_low(self):
        # Very old building: multiplier should be clamped to 0.3
        price_old = estimate_price(50, 1, 0, 1000)
        price_clamped = 50 * 10000 * 0.3
        self.assertEqual(price_old, round(price_clamped, 2))


class EstimatorFormTests(TestCase):
    def test_valid_form(self):
        data = {'square_meters': 90, 'rooms': 3, 'floor': 2, 'age': 10, 'location_rating': 6, 'transport': 'orta'}
        f = EstimateForm(data=data)
        self.assertTrue(f.is_valid())

    def test_invalid_small_room_size(self):
        data = {'square_meters': 30, 'rooms': 4, 'floor': 1, 'age': 5, 'location_rating': 5, 'transport': 'orta'}
        f = EstimateForm(data=data)
        self.assertFalse(f.is_valid())
        self.assertIn('oda oranı çok düşük', str(f.errors))

    def test_invalid_age(self):
        data = {'square_meters': 100, 'rooms': 3, 'floor': 1, 'age': 300, 'location_rating': 5, 'transport': 'orta'}
        f = EstimateForm(data=data)
        self.assertFalse(f.is_valid())
        self.assertIn('Bina yaşı çok büyük', str(f.errors))

    def test_ajax_json_response(self):
        data = {'square_meters': 90, 'rooms': 3, 'floor': 2, 'age': 10, 'location_rating': 7, 'transport': 'kolay'}
        resp = self.client.post('/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        jsond = resp.json()
        self.assertTrue(jsond.get('success'))
        self.assertIn('result', jsond)

    def test_ajax_invalid_json(self):
        data = {'square_meters': 10, 'rooms': 6, 'floor': 1, 'age': 2, 'location_rating': 5, 'transport': 'orta'}
        # small square meters with too many rooms will be invalid
        resp = self.client.post('/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 400)
        jsond = resp.json()
        self.assertFalse(jsond.get('success'))
        self.assertIn('errors', jsond)

    def test_server_side_render_contains_try(self):
        # server-rendered (non-AJAX) POST should include formatted TRY in response
        data = {'square_meters': 120, 'rooms': 3, 'floor': 2, 'age': 5, 'location_rating': 8, 'transport': 'kolay'}
        resp = self.client.post('/', data)
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('₺', content)
