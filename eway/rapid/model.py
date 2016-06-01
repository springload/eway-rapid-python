'''
The module contains model of the library. It is classes reused by different payment methods
and representing data payload to exchange it with eWAY.
'''

from enum import Enum

import inspect
import json
import six


class StructInitMixin(object):
    '''
    Mixin implements a constructor initialising an object attributes from key-value pairs
    '''

    def __init__(self, ignore_unknown=False, **kwargs):
        '''
        Initialize the object with dinamic list of key-value pairs

        Arguments:
            ignore_unknown : bool     = False by default. Whether to ignore all the unknown keys instead of raising an exception
            **kwargs       : {str: ?} = key-value pairs representing attributes of the object and values to be assigned
        '''
        for key in kwargs:
            if key.startswith('__') and key.endswith('__'):
                raise AttributeError('Cannot assign meta field of the object: {}.{}'.format(self.__class__.__name__, key))

            if key not in self.__class__.__dict__.keys():
                if ignore_unknown:
                    continue
                raise AttributeError('Cannot assign non-existing field of the object: {}.{}'.format(self.__class__.__name__, key))

            self.__dict__[key] = kwargs[key]


class StructToJsonMixin(object):
    '''
    Mixin implements a method `to_json` which is to be used for serializing objects of the class
    '''
    def to_json(self, **kwargs):
        '''
        Generates a json string from the object

        Arguments:
            circle : [?] = not to be used explicitly. keeps a list of objects iterated by the function to avoid circular refs
        '''
        if 'circle' not in kwargs:
            circle = []
        else:
            circle = kwargs['circle']

        if self in circle:
            try:
                raise RecursionError('Circular reference detected')
            except NameError:
                raise RuntimeError('Circular reference detected')  # python < 3.5

        circle.append(self)

        _dict = {}

        for key in self.__dict__:
            if isinstance(self.__dict__[key], StructToJsonMixin):
                _dict[key] = self.__dict__[key].to_json(circle=circle, noharm=True)
            elif isinstance(self.__dict__[key], list):
                _dict[key] = []
                for item in self.__dict__[key]:
                    if isinstance(item, StructToJsonMixin):
                        _dict[key].append(item.to_json(circle=circle, noharm=True))
                    else:
                        _dict[key].append(item)
            else:
                _dict[key] = self.__dict__[key]

        return _dict if 'noharm' in kwargs else json.dumps(_dict)


class StructFromJsonMixin(StructInitMixin):
    '''
    Mixin implements a method `from_json` which is to be used for unserializing objects of the class
    '''
    @classmethod
    def from_json(cls, json_string, ignore_unknown=False, **kwargs):
        '''
        Method to unserialize json-encoded objects (recursively)

        Arguments:
            json_string    : str      = json representation of an object of the class
            ignore_unknown : bool     = False by default. Whether to ignore all the unknown keys instead of raising an exception
            **kwargs       : {str: ?} = list of key-value pairs where keys stay for attributes and values contain either:
                                            - a decoder class also implementing StructFromJsonMixin
                                            - list with a single decoder class, showing that the argument must be a list of values
                                            - an instance of a class or a scalar value to be used as a default value
        '''
        if isinstance(json_string, six.string_types):
            _dict = json.loads(json_string)
        elif isinstance(json_string, dict):
            _dict = json_string
        else:
            raise TypeError('The source must be either string or dictionary')

        for key in _dict:
            if key in kwargs:
                if inspect.isclass(kwargs[key]) and issubclass(kwargs[key], StructFromJsonMixin):
                    _dict[key] = kwargs[key].from_json(_dict[key], ignore_unknown)

                elif isinstance(kwargs[key], list) \
                        and len(kwargs[key]) \
                        and inspect.isclass(kwargs[key][0]) \
                        and issubclass(kwargs[key][0], StructFromJsonMixin) \
                        and isinstance(_dict[key], list):
                    for idx in range(0, len(_dict[key])):
                        _dict[key][idx] = kwargs[key][0].from_json(_dict[key][idx], ignore_unknown)

        for key in kwargs:
            if key in _dict:
                continue

            if not inspect.isclass(kwargs[key]):
                _dict[key] = kwargs[key]

            elif isinstance(kwargs[key], list) and (not len(kwargs[key]) or len(kwargs[key]) > 1 or (len(kwargs[key] == 1) and not inspect.isclass(kwargs[key][0]))):
                _dict[key] = kwargs[key]

        instance = cls()
        super(StructFromJsonMixin, instance).__init__(ignore_unknown, **_dict)
        return instance


class StructMixin(StructFromJsonMixin, StructToJsonMixin):
    '''
    Mixin is a shortcut for StructInitMixin, StructFromJsonMixin and StructToJsonMixin altogether
    '''
    pass


class RequestMethod(StructMixin, Enum):
    '''
    Represents a type of a request defined as PaymentMethod in the Rapid API specification, Introduction -> Payment Methods

    NOTE: we cannot use a name PaymentMethod in here, because the name describes rather a kind of an approach we use to perform payment like:
          one of `TransparentRedirect`, `DirectConnection`, `ResponsiveSharedPage` etc
    '''
    ProcessPayment = 'ProcessPayment'
    Authorise = 'Authorise'
    TokenPayment = 'TokenPayment'
    CreateTokenCustomer = 'CreateTokenCustomer'
    UpdateTokenCustomer = 'UpdateTokenCustomer'

    def to_json(self, **kwargs):
        return u'"{}"'.format(self)

    @classmethod
    def from_json(cls, json_string, *args, **kwargs):
        error = ValueError(u'Cannot read a correct representation of RequestMethod from json value: {}'.format(json_string))

        if not json_string.startswith(u'"') and not json_string.startswith(u"'"):
            raise error

        if not json_string.endswith(u'"') and not json_string.endswith(u"'"):
            raise error

        value = json_string[1:-1]

        if value == 'ProcessPayment':
            return cls.ProcessPayment

        elif value == 'Authorise':
            return cls.Authorise

        elif value == 'TokenPayment':
            return cls.TokenPayment

        elif value == 'CreateTokenCustomer':
            return cls.CreateTokenCustomer

        elif value == 'UpdateTokenCustomer':
            return cls.UpdateTokenCustomer

        else:
            raise error


class TransactionType(StructMixin, Enum):
    '''
    Represents transaction types defined by the Rapid API specification
    '''
    Purchase = 'Purchase'
    MOTO = 'MOTO'
    Recurring = 'Recurring'

    def to_json(self, **kwargs):
        return u'"{}"'.format(self)

    @classmethod
    def from_json(cls, json_string, *args, **kwargs):
        error = ValueError(u'Cannot read a correct representation of TransactionType from json value: {}'.format(json_string))

        if not json_string.startswith(u'"') and not json_string.startswith(u"'"):
            raise error

        if not json_string.endswith(u'"') and not json_string.endswith(u"'"):
            raise error

        value = json_string[1:-1]

        if value == 'Purchase':
            return cls.Purchase

        elif value == 'MOTO':
            return cls.MOTO

        elif value == 'Recurring':
            return cls.Recurring

        else:
            raise error


class Payment(StructMixin):
    '''
    Details of the payment being processed

    Attributes:
        TotalAmount  : int  = (conditionally optional) amount of the transaction in the lowest denomination for the currency.
                                                      The value of this field must be 0 for the CreateTokenCustomer and UpdateTokenCustomer request methods.
                                                      This field is required when the request method is ProcessPayment or TokenPayment.

        CurrencyCode : str = (optional) ISO 4217 3 character code that represents the currency that this transaction is to be processed in.
                                        If no value for this field is provided, the merchant's default currency is used.
                                        This should be in uppercase e.g. Australian Dollars = AUD

        InvoiceDescription : str = (optional) A short description of the purchase that the customer is making
        InvoiceNumber      : str = (optional) The merchant's invoice number for this transaction
        InvoiceReference   : str = (optional) The merchant's reference number for this transaction.
    '''

    TotalAmount = None
    CurrencyCode = None
    InvoiceDescription = None
    InvoiceNumber = None
    InvoiceReference = None

    def __init__(self, total_amount=None, currency=None, **kwargs):
        super(Payment, self).__init__(**kwargs)

        if not total_amount:
            total_amount = 0

        if not self.TotalAmount:
            self.TotalAmount = total_amount

        if currency and not self.CurrencyCode:
            self.CurrencyCode = currency


class Customer(StructMixin):
    '''
    Details of the customer

    Attributes:
        CardExpiryMonth : str(2)   = The Token customer's card expiry month
        CardExpiryYear  : str(2)   = The Token customer's card expiry year
        CardIssueNumber : str(2)   = The Token customer's card issue number
        CardName        : str(50)  = The Token customer's card holder name
        CardNumber      : str(50)  = The Token customer's masked credit card number
        CardStartMonth  : str(2)   = The Token customer's card valid from month
        CardStartYear   : str(2)   = The Token customer's card valid from year
        City            : str(50)  = The customer's city / town / suburb
        Comments        : str(255) = Any comments the merchant wishes to add about the customer
        CompanyName     : str(50)  = The customer's company name
        Country         : str(2)   = The customer's country, formatted as a two letter ISO 3166-1 alpha-2 code
        Email           : str(50)  = The customer's email address, which must be correctly formatted if present
        Fax             : str(32)  = The customer's fax number
        FirstName       : str(50)  = The customer's first name
        IsActive        : bool     = If the Token customer is active
        JobDescription  : str(50)  = The customer's job description / title
        LastName        : str(50)  = The customer's last name
        Mobile          : str(32)  = The customer's mobile phone number
        Phone           : str(32)  = The customer's phone number
        PostalCode      : str(50)  = The customer's post / zip code
        Reference       : str(50)  = The merchant's reference for this customer
        State           : str(50)  = The customer's state / county
        Street1         : str(50)  = The customer's street address
        Street2         : str(50)  = The customer's street address
        Title           : str(5)   = The customer's title empty string allowed
        TokenCustomerID : str(16)  = The token customer's unique Token Customer ID
        Url             : str(512) = The customer's website
    '''

    CardExpiryMonth = None
    CardExpiryYear = None
    CardIssueNumber = None
    CardName = None
    CardNumber = None
    CardStartMonth = None
    CardStartYear = None
    City = None
    Comments = None
    CompanyName = None
    Country = None
    Email = None
    Fax = None
    FirstName = None
    IsActive = None
    JobDescription = None
    LastName = None
    Mobile = None
    Phone = None
    PostalCode = None
    Reference = None
    State = None
    Street1 = None
    Street2 = None
    Title = None
    TokenCustomerID = None
    Url = None


class Item(StructMixin):
    '''
    The Items section is optional.
    It is used by Beagle Fraud Alerts (Enterprise) to calculate a risk score for this transaction,
    and by the Responsive Shared page and PayPal to display the order to the customer.

    Attributes:
        SKU         : str(12) = The stock keeping unit or name used to identify this line item
        Description : str(26) = A brief description of the product
        Quantity    : int     = The purchased quantity
        UnitCost    : int     = The pre-tax cost per unit of the product in the lowest denomination (e.g. 500 for $5.00)
        Tax         : int     = The tax amount that applies to this line item in the lowest denomination (e.g. 500 for $5.00)
        Total       : int     = The total amount charged for this line item in the lowest denomination (e.g. 500 for $5.00)
    '''

    SKU = None
    Description = None
    Quantity = None
    UnitCost = None
    Tax = None
    Total = None


class ShippingAddress(StructMixin):
    '''
    The ShippingAddress section is optional.
    It is used by Beagle Fraud Alerts (Enterprise) to calculate a risk score for this transaction

    Attributes:
        FirstName : str(50) = The first name of the person the order is shipped to
        LastName : str(50) = The last name of the person the order is shipped to
        Street1 : str(50) = The street address the order is shipped to
        Street2 : str(50) = The street address of the shipping location
        City : str(50) = The customer's shipping city / town / suburb
        State: str(50) = The customer's shipping state / county
        Country : str(2) = The customer's shipping country. This should be the two letter ISO 3166-1 alpha-2 code. This field must be lower case e.g. Australia = au
        PostalCode : str(30) = The customer's shipping post / zip code
        Email : str(50) = The customer's shipping email address, which must be correctly formatted if present
        Phone : str(32) = The phone number of the person the order is shipped to
        Fax : str(32) = The fax number of the shipping location
        ShippingMethod : str(16) = The method used to ship the customer's order.
                                   One of: Unknown, LowCost, DesignatedByCustomer, International,
                                           Military, NextDay, StorePickup, TwoDayService, ThreeDayService, Other
    '''

    FirstName = None
    LastName = None
    Street1 = None
    Street2 = None
    City = None
    State = None
    Country = None
    PostalCode = None
    Email = None
    Phone = None
    Fax = None
    ShippingMethod = None


class Option(StructMixin):
    '''
    This field is not displayed to the customer but is returned in the result.
    Anything can be used here, which can be useful for tracking transactions.
    Additional characters are truncated at 254

    Attributes:
        Value : str(254) = option value
    '''

    Value = None


class BeagleVerification(StructMixin):
    '''
    Beagle Verification identification checks that may have been performed

    Attributes:
        Email : str(11) = The result of the email verification
        Phone : str(11) = The result of the phone verification
    '''

    Email = None
    Phone = None


class Verification(StructMixin):
    '''
    Currently always empty returned from the eWAY side

    Attributes:
        CVN     : str(10) = ~
        Address : str(10) = ~
        Email   : str(10) = ~
        Mobile  : str(10) = ~
        Phone   : str(10) = ~
    '''

    CVN = None
    Address = None
    Email = None
    Mobile = None
    Phone = None
