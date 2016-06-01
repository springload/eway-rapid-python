import unittest
from hypothesis import given
from hypothesis.strategies import text


try:
    from eway.rapid.model import Option, StructFromJsonMixin, RequestMethod, TransactionType
except:
    from os.path import dirname, join
    from sys import path
    path.append(join(dirname(__file__), '..'))

    from eway.rapid.model import Option, StructFromJsonMixin, RequestMethod, TransactionType


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


class TestStructFromJsonMixin(unittest.TestCase):
    class A1(StructFromJsonMixin):
        a = None
        b = None
        c = None

    def test_a1_from_integer(self):
        with self.assertRaises(TypeError) as err:
            self.A1.from_json(42)

        self.assertEqual(err.exception.args[0], 'The source must be either string or dictionary')

    def test_a1_from_string_with_extra_field(self):
        with self.assertRaises(AttributeError) as err:
            self.A1.from_json('{"a":1, "b":"b is the second letter", "c": null, "d": "extra letter in here"}')

        self.assertEqual(err.exception.args[0], 'Cannot assign non-existing field of the object: A1.d')

    def test_a1_from_string(self):
        obj = self.A1.from_json('{"a":1, "b":"b is the second letter", "c": null, "d": "extra letter in here"}', True)

        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, "b is the second letter")
        self.assertEqual(obj.c, None)

        self.assertEqual(len(obj.__dict__), 3)

    def test_request_method(self):
        method = RequestMethod.Authorise.to_json()
        self.assertEqual(method, '"Authorise"')

        method = RequestMethod.from_json(method)
        self.assertEqual(method, RequestMethod.Authorise)

    def test_transaction_type(self):
        ttype = TransactionType.MOTO.to_json()
        self.assertEqual(ttype, '"MOTO"')

        ttype = TransactionType.from_json(ttype)
        self.assertEqual(ttype, TransactionType.MOTO)
