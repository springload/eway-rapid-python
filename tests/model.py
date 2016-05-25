import unittest
from hypothesis import given
from hypothesis.strategies import text


try:
    import eway
except:
    from os.path import dirname, join
    from sys import path
    path.append(join(dirname(__file__), '..'))

from eway.rapid.model import Option




class TestOption(unittest.TestCase):
    @given(text())
    def test_init(self, value):
        option = Option(Value=value)
        self.assertEqual(option.Value, value)

    @given(text())
    def test_json(self, value):
        option = Option(Value=value)

        option_to_json = option.to_json()
        option_from_json = Option.from_json(option_to_json)

        self.assertEqual(option_from_json.Value, option.Value)