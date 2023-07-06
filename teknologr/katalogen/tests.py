from django.test import TestCase
from datetime import date
from .utils import *

class CreateDurationsStringTest(TestCase):
    def setUp(self):
        self.d1 = date(1998, 1, 1)
        self.d2 = date(1998, 1, 30)
        self.d3 = date(1998, 12, 31)
        self.d4 = date(2000, 12, 31)
        self.d5 = date(2001, 7, 7)
        self.d6 = date(2002, 12, 31)

    def test_same_date(self):
        self.assertEqual('1 januari 1998', create_duration_string(self.d1, self.d1))

    def test_same_month(self):
        self.assertEqual('1-30 januari 1998', create_duration_string(self.d1, self.d2))

    def test_same_year(self):
        self.assertEqual('30 januari - 31 december 1998', create_duration_string(self.d2, self.d3))

    def test_whole_years(self):
        self.assertEqual('1998', create_duration_string(self.d1, self.d3))
        self.assertEqual('1998-2000', create_duration_string(self.d1, self.d4))

    def test_no_simplification(self):
        self.assertEqual('1 januari 1998 - 7 juli 2001', create_duration_string(self.d1, self.d5))
        self.assertEqual('7 juli 2001 - 31 december 2002', create_duration_string(self.d5, self.d6))


# Create your tests here.
