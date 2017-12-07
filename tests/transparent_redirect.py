import requests

import unittest
from hypothesis import given
from hypothesis.strategies import text



try:
    import eway
except:
    from os.path import dirname, join
    from sys import path
    path.append(join(dirname(__file__), '..'))


from eway.rapid.client import RestClient
from eway.rapid.exception import EwayError
from eway.rapid.model import Customer, Item, Option, Payment, RequestMethod, ShippingAddress, TransactionType
from eway.rapid.endpoint import SandboxEndpoint
from eway.rapid.payment_method.transparent_redirect import TransparentRedirect, CreateAccessCodeRequest, AccessCodeResponse
from eway.rapid.payment_method.transparent_redirect.response import TransactionInfo



class TestTransparentRedirect(unittest.TestCase):
    method = None

    @classmethod
    def setUpClass(cls):
        credentials = r"60CF3Ce97nRS1Z1Wp5m9kMmzHHEh8Rkuj31QCtVxjPWGYA9FymyqsK0Enm1P6mHJf0THbR", r"API-P4ss"
        client = RestClient(credentials[0], credentials[1], SandboxEndpoint())
        cls.method = TransparentRedirect(client)


    def test_createAccessCode(self):
        response = self.method.create_access_code(CreateAccessCodeRequest(
            Payment(42),
            RequestMethod.ProcessPayment,
            TransactionType.Purchase,
            'https://localhost/'
        ))

        self.assertIsInstance(response, AccessCodeResponse)

        self.assertIsNotNone(response.AccessCode)
        self.assertIsNotNone(response.Payment)
        self.assertIsNotNone(response.Customer)

        self.assertIsInstance(response.Payment, Payment)
        self.assertIsInstance(response.Customer, Customer)

        self.assertEqual(response.Payment.TotalAmount, 42)


    def test_payment(self):
        response = self.method.create_access_code(CreateAccessCodeRequest(
            Payment(
                TotalAmount = 42,
                CurrencyCode = 'AUD',
                InvoiceDescription = r'My test invoice described in here',
                InvoiceNumber = 'TEST-TR-1',
                InvoiceReference = 'TEST-TR-1-REF'
            ),
            RequestMethod.ProcessPayment,
            TransactionType.Purchase,
            'https://localhost/',
            Customer = Customer(
                City = 'Wellington',
                Comments = 'Just some comments in here',
                CompanyName = 'Springload',
                Country = 'nz',
                Email = 'mrtester@springload.co.nz',
                Fax = '000011112222',
                FirstName = 'Mr',
                JobDescription = 'QA',
                LastName = 'Tester',
                Mobile = '000022221111',
                Phone = '000033332222',
                PostalCode = '6011',
                Reference = 'BESTTESTEREVER',
                State = 'NZ',
                Street1 = 'Testing street',
                Street2 = "Testers' building",
                Title = 'Mrs.',
                Url = 'http://springload.co.nz/'
            ),
            ShippingAddress = ShippingAddress(
                ShippingMethod = 'NextDay',
                FirstName = 'Mr',
                LastName = 'Tester',
                Street1 = 'Testing street',
                Street2 = "Testers' building",
                City = 'Wellington',
                State = 'NZ',
                Country = 'NZ',
                PostalCode = '6011',
                Email = 'mrtester@springload.co.nz',
                Phone = '000033332222',
                Fax = '000011112222'
            ),
            Items = [
                Item(
                    SKU = 'Item1',
                    Description = 'Item1 description',
                    Quantity = 4,
                    UnitCost = 3.14,
                    Tax = 1.86 * 4,
                    Total = 5 * 4
                ),
                Item(
                    SKU = 'Item2',
                    Description = 'Item2 description',
                    Quantity = 6,
                    UnitCost = 3.14,
                    Tax = 2.86 * 6,
                    Total = 6 * 6
                )
            ],
            Options = [
                Option(Value='Option1'),
                Option(Value='Option2'),
                Option(Value='Option3'),
                Option(Value='Option4'),
                Option(Value='Option5')
            ]
        ))

        self.assertIsInstance(response, AccessCodeResponse)

        self.assertIsNotNone(response.AccessCode)
        self.assertIsNotNone(response.Payment)
        self.assertIsNotNone(response.Customer)
        self.assertIsNotNone(response.FormActionURL)


        self.assertIsInstance(response.Payment, Payment)
        self.assertEqual(response.Payment.TotalAmount, 42)
        self.assertEqual(response.Payment.CurrencyCode, 'AUD')
        self.assertEqual(response.Payment.InvoiceDescription, r'My test invoice described in here')
        self.assertEqual(response.Payment.InvoiceNumber, 'TEST-TR-1')
        self.assertEqual(response.Payment.InvoiceReference, 'TEST-TR-1-REF')

        self.assertIsInstance(response.Customer, Customer)
        self.assertEqual(response.Customer.City, 'Wellington')
        self.assertEqual(response.Customer.Comments, 'Just some comments in here')
        self.assertEqual(response.Customer.CompanyName, 'Springload')
        self.assertEqual(response.Customer.Country, 'nz')
        self.assertEqual(response.Customer.Email, 'mrtester@springload.co.nz')
        self.assertEqual(response.Customer.Fax, '000011112222')
        self.assertEqual(response.Customer.FirstName, 'Mr')
        self.assertEqual(response.Customer.IsActive, False)
        self.assertEqual(response.Customer.JobDescription, 'QA')
        self.assertEqual(response.Customer.LastName, 'Tester')
        self.assertEqual(response.Customer.Mobile, '000022221111')
        self.assertEqual(response.Customer.Phone, '000033332222')
        self.assertEqual(response.Customer.PostalCode, '6011')
        self.assertEqual(response.Customer.Reference, 'BESTTESTEREVER')
        self.assertEqual(response.Customer.State, 'NZ')
        self.assertEqual(response.Customer.Street1, 'Testing street')
        self.assertEqual(response.Customer.Street2, 'Testers&#39; building')
        self.assertEqual(response.Customer.Title, 'Mrs.')
        self.assertEqual(response.Customer.Url, 'http://springload.co.nz/')


        voila = requests.post(response.FormActionURL, allow_redirects=False, data={
            'EWAY_ACCESSCODE': response.AccessCode,
            'EWAY_PAYMENTTYPE': 'Credit Card',
            'EWAY_CARDNAME': 'Mr Tester',
            'EWAY_CARDNUMBER': '4444333322221111',
            'EWAY_CARDEXPIRYMONTH': '11',
            'EWAY_CARDEXPIRYYEAR' : '28',
            'EWAY_CARDCVN': '666'
        })

        self.assertEqual(voila.status_code, 302)
        self.assertIsNotNone(voila.headers.get('Location'))
        self.assertEqual(voila.headers.get('Location'), 'https://localhost/?AccessCode={}'.format(response.AccessCode))


        info = self.method.request_transaction_result(response.AccessCode)

        self.assertEqual(info.AccessCode, response.AccessCode)
        self.assertIsNotNone(info.AuthorisationCode)
        self.assertIsNotNone(info.ResponseCode)
        self.assertIsNotNone(info.TransactionID)

        self.assertEqual(info.ResponseMessage, 'A2000')
        self.assertEqual(info.InvoiceNumber, 'TEST-TR-1')
        self.assertEqual(info.InvoiceReference, 'TEST-TR-1-REF')
        self.assertEqual(info.TotalAmount, 42)
        self.assertTrue(info.TransactionStatus)
        self.assertIsNone(info.TokenCustomerID)
        self.assertEqual(info.BeagleScore, 0)
        self.assertIsNone(info.Errors)

        self.assertIsNotNone(info.Options)
        self.assertEqual(len(info.Options), 5)
        self.assertEqual(info.Options[0].Value, 'Option1')
        self.assertEqual(info.Options[1].Value, 'Option2')
        self.assertEqual(info.Options[2].Value, 'Option3')
        self.assertEqual(info.Options[3].Value, 'Option4')
        self.assertEqual(info.Options[4].Value, 'Option5')


class TestTransactionInfo(unittest.TestCase):
    def test_undocumented_message_key_does_not_raise(self):
        data = '{"Message":"Access Code Not Found"}'
        try:
            TransactionInfo.from_json(data, ignore_unknown=False)
        except AttributeError:
            self.fail('TransactionInfo should not raise `AttributeError` for `Message` key in data')

    def test_undocumented_message_key_is_not_available(self):
        data = '{"Message":"Access Code Not Found"}'
        struct = TransactionInfo.from_json(data, ignore_unknown=False)

        with self.assertRaises(AttributeError):
            struct.Message

    def test_undocumented_message_map_success(self):
        message = 'Access Code Not Found'
        data = '{"Message":"%s"}' % message
        struct = TransactionInfo.from_json(data, ignore_unknown=False)
        code = EwayError.lookup_error_by_message(message)._code

        self.assertIsNotNone(struct.ResponseMessage, msg='Message should map to ResponseMessage')
        self.assertEqual(struct.ResponseMessage, code, msg='Message should map to ResponseMessage')

    def test_undocumented_message_map_ignored(self):
        message = 'Access Code Not Found'
        response_message = 'FooBar'
        data = '{"Message":"%s","ResponseMessage":"%s"}' % (message, response_message)
        struct = TransactionInfo.from_json(data, ignore_unknown=False)
        code = EwayError.lookup_error_by_message(message)._code

        self.assertEqual(struct.ResponseMessage, response_message, msg='Message should not overwrite ResponseMessage')
        self.assertNotEqual(struct.ResponseMessage, code, msg='Message should not overwrite ResponseMessage')