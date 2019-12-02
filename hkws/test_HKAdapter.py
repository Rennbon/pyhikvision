from unittest import TestCase

from hkws.soadapter import HKAdapter


class TestHKAdapter(TestCase):
    def test_add_so(self):
        a = HKAdapter()
        a.add_so("../lib/")
        print(a.so_list)

    def test_init_sdk(self):
        a = HKAdapter()
        a.add_so("/justdo/python/bblock/lib/")
        bl = a.init_sdk()
