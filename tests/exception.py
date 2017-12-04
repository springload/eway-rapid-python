import unittest

try:
    import eway
except:
    from os.path import dirname, join
    from sys import path
    path.append(join(dirname(__file__), '..'))


from eway.rapid.exception import EwayError, UndocumentedError


class TestEwayError(unittest.TestCase):
    def test_undocumented_access_code_not_found_message_has_a_custom_code(self):
        err = EwayError.lookup_error_by_message('Access Code Not Found')
        expected_code = 'UE001'
        
        self.assertEqual(err._code, expected_code)

    def test_undocumented_known_message_returns_undocumented_error(self):
        err = EwayError.lookup_error_by_message('Access Code Not Found')

        self.assertIsInstance(err, UndocumentedError)

    def test_undocumented_unknown_message_returns_none(self):
        err = EwayError.lookup_error_by_message('FooBar')

        self.assertIsNone(err)