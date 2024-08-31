import unittest
from collections import namedtuple

from weewx.drivers.ws23xx import BcdNumsConverter, NonBcdDigitError


class BcdTest(unittest.TestCase):
    def test_conversion(self):
        Param = namedtuple("Param", "conversion,nybbles,numbers")
        cases = [
            Param([1], bytes([1]), [1]),
            Param([2], bytes([1, 2]), [21]),
            Param([4], [0, 1, 2, 0], [210]),
            Param([1, 2, 3], bytes([1, 2, 3, 4, 5, 6]), [1, 32, 654]),
            Param([1, 2, 3], bytes([1, 0, 3, 4, 5, 0]), [1, 30, 54]),
        ]
        for idx, param in enumerate(cases):
            with self.subTest(msg=f"case #{idx}", param=param):
                bcd = BcdNumsConverter(param.conversion)
                self.assertListEqual(param.numbers, bcd.to_numbers(param.nybbles))
                self.assertListEqual(
                    list(param.nybbles), bcd.from_numbers(param.numbers)
                )

    def test_to_numbers_raises_on_non_bcd_digit(self):
        with self.assertRaises(NonBcdDigitError) as cm:
            BcdNumsConverter([2]).to_numbers(b"\x0a\x00")
        self.assertEqual(cm.exception.digit, 10)
