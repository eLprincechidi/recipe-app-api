"""sample tests"""

from django.test import SimpleTestCase
from app.calc import add
from app.calc import subtract
from app.calc import test_get_greeting
from rest_framework.test import APIClient


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        
        res = add(3, 4)
        self.assertEqual(res, 7)
        
    
    
    def test_subtract_numbers(self):
        res = subtract(10, 5)
        self.assertEqual(res, 5)
        
        
class TestView(SimpleTestCase):
    """test getting api view"""
    def test_get_greeting(self):
        client = APIClient()
        res = client.get('/greeting/')
    
        
        self.assertEqual(res.data, {'greeting': 'Hello, World'},)
        