from unittest import TestCase

from hkws.soadapter import HKAdapter


class TestHKAdapter(TestCase):
    def test_add_lib(self):
        a = HKAdapter()
        a.add_lib("/Users/zhubin/python/pyhikvsion/hkws/lib/linux",".so")
        print(a.so_list)

