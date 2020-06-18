from django.test import TestCase
import time
from .models import *

class TimeTest(TestCase):
    def test_simple_access_time(self):
         start = time.time()
         Bilet.objects.values_list('nr_biletu')
         end = time.time()
         self.assertLessEqual(end - start, 2)

    def test_complex_access_time(self):
         start = time.time()
         Bilet.objects.filter(wykupiony_czas__range = [200, 300]).values_list('nr_biletu')
         end = time.time()
         self.assertLessEqual(end - start, 5)

    def test_add_2k_tickets(self):
        for i in range(2000):
            b = Bilet(nr_biletu=5000+i, czas_wjazdu="2020-06-02 12:12:12",
                      czas_wyjazdu="2020-06-02 14:14:12", wykupiony_czas=180)
            b.strefa = Strefa.objects.get(id=1)
            b.save()

        tickets = Bilet.objects.filter(wykupiony_czas__gte = 100).values_list('nr_biletu')
        self.assertGreaterEqual(len(tickets), 2000)