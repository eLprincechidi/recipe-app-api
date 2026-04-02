"""sample tests"""
from django.test import SimpleTestCase
from app.calc import add
from app.calc import subtract


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        res = add(3, 4)
        self.assertEqual(res, 7)

    def test_subtract_numbers(self):
        res = subtract(10, 5)
        self.assertEqual(res, 5)
