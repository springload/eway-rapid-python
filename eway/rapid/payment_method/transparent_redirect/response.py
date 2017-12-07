'''
The module contains classes representing responses of the Rapid API during creation of a transaction
using TransparentRedirect payment method
'''

import json
import six

from eway.rapid.exception import EwayError
from eway.rapid.model import Customer, Option, Payment, StructMixin, Verification, BeagleVerification


class AccessCodeResponse(StructMixin):
    '''
    Response for the Step1: CREATE A NEW ACCESS CODE

    Attributes:
        AccessCode          : str             = A unique access code that is used to identify this transaction with Rapid API.
                                                This code will need to be present for all future requests associated with this transaction.
        FormActionURL       : str             = The URL that the form should be POSTed to in Step 2
        CompleteCheckoutURL : str             = PayPal Checkout URL
        Errors              : str             = Comma separated list of any error encountered
        Customer            : .model.Customer = echo of the payment information submitted in the request
        Payment             : .model.Payment  = echo of the payment information submitted in the request
    '''

    AccessCode = None
    FormActionURL = None
    CompleteCheckoutURL = None
    Errors = None
    Customer = None
    Payment = None

    @classmethod
    def from_json(cls, json_string, ignore_unknown=False, **kwargs):
        _kwargs = {'Customer': Customer, 'Payment': Payment}
        _kwargs.update(kwargs)
        return super(AccessCodeResponse, cls).from_json(json_string, ignore_unknown, **_kwargs)


class TransactionInfo(StructMixin):
    '''
    Response for the Step3: REQUEST THE RESULTS

    Attributes:
        AccessCode        : str(512) = An echo of the access code used in the request
        AuthorisationCode : str(6)   = The authorisation code for this transaction as returned by the bank
        ResponseCode      : str(2)   = The two digit response code returned from the bank
        ResponseMessage   : str(512) = One or more Response Codes that describes the result of the action performed.
                                       If a Beagle Alert is triggered, this may contain multiple codes: e.g. D4405, F7003
        InvoiceNumber     : str(64)  = An echo of the merchant's invoice number for this transaction
        InvoiceReference  : str(64)  = An echo of the merchant's reference number for this transaction
        TotalAmount       : int      = The amount that was authorised for this transaction
        TransactionID     : int      = A unique identifier that represents the transaction in eWAY's system
        TransactionStatus : bool     = A Boolean value that indicates whether the transaction was successful or not
        TokenCustomerID   : int      = An eWAY-issued ID that represents the Token customer that was loaded or created for this transaction (if applicable)
        BeagleScore       : string   = Fraud score representing the estimated probability that the order is fraud.
                                       A value between 0.01 to 100.00 representing the % risk the transaction is fraudulent.
        Errors            : string   = A comma separated list of any error encountered

        Options            : [str(255)]                = Options collection passed in the original request will be echoed back in the response here
        Verification       : .model.Verification       = These fields are currently unused
        BeagleVerification : .model.BeagleVerification = Always empty for TransparentRedirect
    '''

    AccessCode = None
    AuthorisationCode = None
    ResponseCode = None
    ResponseMessage = None
    InvoiceNumber = None
    InvoiceReference = None
    TotalAmount = None
    TransactionID = None
    TransactionStatus = None
    TokenCustomerID = None
    BeagleScore = None
    Errors = None
    Options = None
    Verification = None
    BeagleVerification = None

    @classmethod
    def from_json(cls, json_string, ignore_unknown=False, **kwargs):
        _kwargs = {'Options': [Option], 'Verification': Verification, 'BeagleVerification': BeagleVerification}
        _kwargs.update(kwargs)

        if isinstance(json_string, six.string_types):
            _dict = json.loads(json_string)
        elif isinstance(json_string, dict):
            _dict = json_string
        else:
            raise TypeError('The source must be either string or dictionary')

        cls._map_undocumented_message(_dict)

        return super(TransactionInfo, cls).from_json(_dict, ignore_unknown, **_kwargs)

    @classmethod
    def _map_undocumented_message(cls, _dict):
        if 'Message' not in _dict:
            return

        # Pop the key so it doesn't crash during init.
        msg = _dict.pop('Message')

        # Do not overwrite the official `ResponseMessage` with the unofficial `Message`.
        if 'ResponseMessage' in _dict:
            return

        err = EwayError.lookup_error_by_message(msg)
        _dict['ResponseMessage'] = err._code if err else msg
