import logging
import unittest

from crypto_VDF.utils.logger import get_logger, set_level

log = get_logger()


class TestLogger(unittest.TestCase):

    def test_logger_dec_without_level(self):
        @set_level(log)
        def func(_a: int, _verbose=False):
            pass

        log.setLevel(logging.INFO)

        func(_a=1)
        self.assertEqual(log.level, logging.INFO)
        func(1)
        self.assertEqual(log.level, logging.INFO)

        func(_a=1, _verbose=True)
        self.assertEqual(log.level, logging.DEBUG)

        log.setLevel(logging.INFO)

        func(1, True)
        self.assertEqual(log.level, logging.DEBUG)

    def test_logger_dec_with_level(self):
        @set_level(logger=log, level=logging.ERROR)
        def func(_a: int, _verbose=False):
            pass

        log.setLevel(logging.INFO)

        func(_a=1)
        self.assertEqual(log.level, logging.INFO)
        func(1)
        self.assertEqual(log.level, logging.INFO)

        func(_a=1, _verbose=True)
        self.assertEqual(log.level, logging.ERROR)

        log.setLevel(logging.INFO)

        func(1, True)
        self.assertEqual(log.level, logging.ERROR)
