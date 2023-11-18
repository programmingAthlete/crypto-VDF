import unittest

from crypto_VDF.dummy_file import dummy_func


class TestDummyFunc(unittest.TestCase):

    def test_dummy_func(self):
        self.assertEqual(dummy_func(), 1)
