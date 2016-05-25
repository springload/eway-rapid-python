class EwayError(Exception):
    '''
    Base exception of the library
    '''

    _code = None
    _message = None
    _response_struct = None
    _response_string = None

    def __init__(self, code, message, response=None, *args, **kwargs):
        '''
        Initializes the exception

        Arguments:
            code    : str = Rapid API response/error code
            message : str = appropriate message
        '''

        if 'response_struct' in kwargs:
            self._response_struct = kwargs.pop('response_struct')

        if 'response_string' in kwargs:
            self._response_string = kwargs.pop('response_string')

        super(EwayError, self).__init__(*args, **kwargs)

        self._code = code
        self._message = '{} / {}'.format(code, message).encode('utf-8')


    def __bytes__(self):
        return self._message

    def __unicode__(self):
        try:
            return unicode(self.__bytes__())
        except NameError:
            return str(self.__bytes__(), 'utf-8')

    def __str__(self):
        return self.__bytes__().decode('utf-8')

    def __repr__(self):
        return self.__unicode__()


    @classmethod
    def from_code(cls, code, *args, **kwargs):
        '''
        Create an error object from code
        '''

        if code in cls.INDEX:
            return cls(code, *args, **kwargs)

        return None


    @staticmethod
    def lookup_error_by_code(code, *args, **kwargs):
        response_error = ResponseError.from_code(code)
        if response_error:
            return response_error

        validation_error = ValidationError.from_code(code, *args, **kwargs)
        if validation_error:
            return validation_error

        transaction_error = TransactionError.from_code(code, *args, **kwargs)
        if transaction_error:
            return transaction_error

        fraud_error = FraudError.from_code(code)
        if fraud_error:
            return fraud_error

        system_error = SystemError.from_code(code)
        if system_error:
            return system_error



class ResponseError(EwayError):
    INDEX = {
        'S9990': 'Rapid endpoint not set or invalid',
        'S9901': 'Response is not JSON',
        'S9902': 'Empty response',
        'S9991': 'Rapid API key or password not set',
        'S9992': 'Error connecting to Rapid gateway',
        'S9993': 'Authentication error',
        'S9995': 'Error converting to or from JSON, invalid parameter',
        'S9996': 'Rapid gateway server error'
    }

    def __init__(self, code, *args, **kwargs):
        if code not in ResponseError.INDEX.keys():
            raise ValueError('Invalid error code: {}'.format(code))

        super(ResponseError, self).__init__(code, ResponseError.INDEX[code], *args, **kwargs)


class ValidationError(EwayError):
    INDEX = {
        "V6000": "Validation error",
        "V6001": "Invalid CustomerIP",
        "V6002": "Invalid DeviceID",
        "V6003": "Invalid Request PartnerID",
        "V6004": "Invalid Request Method",
        "V6010": "Invalid TransactionType, account not certified for eCome only MOTO or Recurring available",
        "V6011": "Invalid Payment TotalAmount",
        "V6012": "Invalid Payment InvoiceDescription",
        "V6013": "Invalid Payment InvoiceNumber",
        "V6014": "Invalid Payment InvoiceReference",
        "V6015": "Invalid Payment CurrencyCode",
        "V6016": "Payment Required",
        "V6017": "Payment CurrencyCode Required",
        "V6018": "Unknown Payment CurrencyCode",
        "V6021": "EWAY_CARDHOLDERNAME Required",
        "V6022": "EWAY_CARDNUMBER Required",
        "V6023": "EWAY_CARDCVN Required",
        "V6033": "Invalid Expiry Date",
        "V6034": "Invalid Issue Number",
        "V6035": "Invalid Valid From Date",
        "V6040": "Invalid TokenCustomerID",
        "V6041": "Customer Required",
        "V6042": "Customer FirstName Required",
        "V6043": "Customer LastName Required",
        "V6044": "Customer CountryCode Required",
        "V6045": "Customer Title Required",
        "V6046": "TokenCustomerID Required",
        "V6047": "RedirectURL Required",
        "V6048": "CheckoutURL Required when CheckoutPayment specified",
        "V6049": "Invalid Checkout URL",
        "V6051": "Invalid Customer FirstName",
        "V6052": "Invalid Customer LastName",
        "V6053": "Invalid Customer CountryCode",
        "V6058": "Invalid Customer Title",
        "V6059": "Invalid RedirectURL",
        "V6060": "Invalid TokenCustomerID",
        "V6061": "Invalid Customer Reference",
        "V6062": "Invalid Customer CompanyName",
        "V6063": "Invalid Customer JobDescription",
        "V6064": "Invalid Customer Street1",
        "V6065": "Invalid Customer Street2",
        "V6066": "Invalid Customer City",
        "V6067": "Invalid Customer State",
        "V6068": "Invalid Customer PostalCode",
        "V6069": "Invalid Customer Email",
        "V6070": "Invalid Customer Phone",
        "V6071": "Invalid Customer Mobile",
        "V6072": "Invalid Customer Comments",
        "V6073": "Invalid Customer Fax",
        "V6074": "Invalid Customer URL",
        "V6075": "Invalid ShippingAddress FirstName",
        "V6076": "Invalid ShippingAddress LastName",
        "V6077": "Invalid ShippingAddress Street1",
        "V6078": "Invalid ShippingAddress Street2",
        "V6079": "Invalid ShippingAddress City",
        "V6080": "Invalid ShippingAddress State",
        "V6081": "Invalid ShippingAddress PostalCode",
        "V6082": "Invalid ShippingAddress Email",
        "V6083": "Invalid ShippingAddress Phone",
        "V6084": "Invalid ShippingAddress Country",
        "V6085": "Invalid ShippingAddress ShippingMethod",
        "V6086": "Invalid ShippingAddress Fax",
        "V6091": "Unknown Customer CountryCode",
        "V6092": "Unknown ShippingAddress CountryCode",
        "V6100": "Invalid EWAY_CARDNAME",
        "V6101": "Invalid EWAY_CARDEXPIRYMONTH",
        "V6102": "Invalid EWAY_CARDEXPIRYYEAR",
        "V6103": "Invalid EWAY_CARDSTARTMONTH",
        "V6104": "Invalid EWAY_CARDSTARTYEAR",
        "V6105": "Invalid EWAY_CARDISSUENUMBER",
        "V6106": "Invalid EWAY_CARDCVN",
        "V6107": "Invalid EWAY_ACCESSCODE",
        "V6108": "Invalid CustomerHostAddress",
        "V6109": "Invalid UserAgent",
        "V6110": "Invalid EWAY_CARDNUMBER",
        "V6111": "Unauthorised API Access, Account Not PCI Certified",
        "V6112": "Redundant card details other than expiry year and month",
        "V6113": "Invalid transaction for refund",
        "V6114": "Gateway validation error",
        "V6115": "Invalid DirectRefundRequest, Transaction ID",
        "V6116": "Invalid card data on original TransactionID",
        "V6117": "Invalid CreateAccessCodeSharedRequest, FooterText",
        "V6118": "Invalid CreateAccessCodeSharedRequest, HeaderText",
        "V6119": "Invalid CreateAccessCodeSharedRequest, Language",
        "V6120": "Invalid CreateAccessCodeSharedRequest, LogoUrl",
        "V6121": "Invalid TransactionSearch, Filter Match Type",
        "V6122": "Invalid TransactionSearch, Non numeric Transaction ID",
        "V6123": "Invalid TransactionSearch,no TransactionID or AccessCode specified",
        "V6124": "Invalid Line Items. The line items have been provided however the totals do not match the TotalAmount field",
        "V6125": "Selected Payment Type not enabled",
        "V6126": "Invalid encrypted card number, decryption failed",
        "V6127": "Invalid encrypted cvn, decryption failed",
        "V6128": "Invalid Method for Payment Type",
        "V6129": "Transaction has not been authorised for Capture/Cancellation",
        "V6130": "Generic customer information error",
        "V6131": "Generic shipping information error",
        "V6132": "Transaction has already been completed or voided, operation not permitted",
        "V6133": "Checkout not available for Payment Type",
        "V6134": "Invalid Auth Transaction ID for Capture/Void",
        "V6135": "PayPal Error Processing Refund",
        "V6140": "Merchant account is suspended",
        "V6141": "Invalid PayPal account details or API signature",
        "V6142": "Authorise not available for Bank/Branch",
        "V6150": "Invalid Refund Amount",
        "V6151": "Refund amount greater than original transaction",
        "V6152": "Original transaction already refunded for total amount",
        "V6153": "Card type not support by merchant",
        "V6160": "Encryption Method Not Supported",
        "V6161": "Encryption failed, missing or invalid key",
        "V6165": "Invalid Visa Checkout data or decryption failed",
        "V6170": "Invalid TransactionSearch, Invoice Number is not unique",
        "V6171": "Invalid TransactionSearch, Invoice Number not found"
    }


    def __init__(self, code, *args, **kwargs):
        if code not in ValidationError.INDEX.keys():
            raise ValueError('Invalid error code: {}'.format(code))

        super(ValidationError, self).__init__(code, ValidationError.INDEX[code], *args, **kwargs)



class SystemError(EwayError):
    INDEX = {
        'S5000': 'System Error',
        'S5011': 'PayPal Connection Error',
        'S5012': 'PayPal Settings Error',
        'S5085': 'Started 3dSecure',
        'S5086': 'Routed 3dSecure',
        'S5087': 'Completed 3dSecure',
        'S5088': 'PayPal Transaction Created',
        'S5099': 'Incomplete (Access Code in progress/incomplete)',
        'S5010': 'Unknown error returned by gateway'
    }

    def __init__(self, code, *args, **kwargs):
        if code not in SystemError.INDEX.keys():
            raise ValueError('Invalid error code: {}'.format(code))

        super(SystemError, self).__init__(code, SystemError.INDEX[code], *args, **kwargs)


class FraudError(EwayError):
    INDEX = {
        "F7000": "Undefined Fraud Error",
        "F7001": "Challenged Fraud",
        "F7002": "Country Match Fraud",
        "F7003": "High Risk Country Fraud",
        "F7004": "Anonymous Proxy Fraud",
        "F7005": "Transparent Proxy Fraud",
        "F7006": "Free Email Fraud",
        "F7007": "International Transaction Fraud",
        "F7008": "Risk Score Fraud",
        "F7009": "Denied Fraud",
        "F7010": "Denied by PayPal Fraud Rules",
        "F9001": "Custom Fraud Rule",
        "F9010": "High Risk Billing Country",
        "F9011": "High Risk Credit Card Country",
        "F9012": "High Risk Customer IP Address",
        "F9013": "High Risk Email Address",
        "F9014": "High Risk Shipping Country",
        "F9015": "Multiple card numbers for single email address",
        "F9016": "Multiple card numbers for single location",
        "F9017": "Multiple email addresses for single card number",
        "F9018": "Multiple email addresses for single location",
        "F9019": "Multiple locations for single card number",
        "F9020": "Multiple locations for single email address",
        "F9021": "Suspicious Customer First Name",
        "F9022": "Suspicious Customer Last Name",
        "F9023": "Transaction Declined",
        "F9024": "Multiple transactions for same address with known credit card",
        "F9025": "Multiple transactions for same address with new credit card",
        "F9026": "Multiple transactions for same email with new credit card",
        "F9027": "Multiple transactions for same email with known credit card",
        "F9028": "Multiple transactions for new credit card",
        "F9029": "Multiple transactions for known credit card",
        "F9030": "Multiple transactions for same email address",
        "F9031": "Multiple transactions for same credit card",
        "F9032": "Invalid Customer Last Name",
        "F9033": "Invalid Billing Street",
        "F9034": "Invalid Shipping Street",
        "F9037": "Suspicious Customer Email Address",
        "F9049": "Genuine Customer",
        "F9050": "High Risk Email Address and amount",
        "F9113": "Card issuing country differs from IP address country"
    }

    def __init__(self, code, *args, **kwargs):
        if code not in FraudError.INDEX.keys():
            raise ValueError('Invalid error code: {}'.format(code))

        super(FraudError, self).__init__(code, FraudError.INDEX[code], *args, **kwargs)



class TransactionError(EwayError):
    INDEX = {
        "A2000": "Transaction Approved Successful*",
        "A2008": "Honour With Identification Successful",
        "A2010": "Approved For Partial Amount Successful",
        "A2011": "Approved, VIP Successful",
        "A2016": "Approved, Update Track 3 Successful",
        "D4401": "Refer to Issuer Failed",
        "D4402": "Refer to Issuer, special Failed",
        "D4403": "No Merchant Failed",
        "D4404": "Pick Up Card Failed",
        "D4405": "Do Not Honour Failed",
        "D4406": "Error Failed",
        "D4407": "Pick Up Card, Special Failed",
        "D4409": "Request In Progress Failed",
        "D4412": "Invalid Transaction Failed",
        "D4413": "Invalid Amount Failed",
        "D4414": "Invalid Card Number Failed",
        "D4415": "No Issuer Failed",
        "D4419": "Re-enter Last Transaction Failed",
        "D4421": "No Action Taken Failed",
        "D4422": "Suspected Malfunction Failed",
        "D4423": "Unacceptable Transaction Fee Failed",
        "D4425": "Unable to Locate Record On File Failed",
        "D4430": "Format Error Failed",
        "D4431": "Bank Not Supported By Switch Failed",
        "D4433": "Expired Card, Capture Failed",
        "D4434": "Suspected Fraud, Retain Card Failed",
        "D4435": "Card Acceptor, Contact Acquirer, Retain Card Failed",
        "D4436": "Restricted Card, Retain Card Failed",
        "D4437": "Contact Acquirer Security Department, Retain Card Failed",
        "D4438": "PIN Tries Exceeded, Capture Failed",
        "D4439": "No Credit Account Failed",
        "D4440": "Function Not Supported Failed",
        "D4441": "Lost Card Failed",
        "D4442": "No Universal Account Failed",
        "d4443": "Stolen Card Failed",
        "D4444": "No Investment Account Failed",
        "D4450": "Visa Checkout Transaction Error",
        "D4451": "Insufficient Funds Failed",
        "D4452": "No Cheque Account Failed",
        "D4453": "No Savings Account Failed",
        "D4454": "Expired Card Failed",
        "D4455": "Incorrect PIN Failed",
        "D4456": "No Card Record Failed",
        "D4457": "Function Not Permitted to Cardholder Failed",
        "D4458": "Function Not Permitted to Terminal Failed",
        "D4459": "Suspected Fraud Failed",
        "D4460": "Acceptor Contact Acquirer Failed",
        "D4461": "Exceeds Withdrawal Limit Failed",
        "D4462": "Restricted Card Failed",
        "D4463": "Security Violation Failed",
        "D4464": "Original Amount Incorrect Failed",
        "D4466": "Acceptor Contact Acquirer, Security Failed",
        "D4467": "Capture Card Failed",
        "D4475": "PIN Tries Exceeded Failed",
        "D4482": "CVV Validation Error Failed",
        "D4490": "Cut off In Progress Failed",
        "D4491": "Card Issuer Unavailable Failed",
        "D4492": "Unable To Route Transaction Failed",
        "D4493": "Cannot Complete, Violation Of The Law Failed",
        "D4494": "Duplicate Transaction Failed",
        "D4495": "Amex Declined Failed",
        "D4496": "System Error Failed",
        "D4497": "MasterPass Error Failed",
        "D4498": "PayPal Create Transaction Error Failed",
        "D4499": "Invalid Transaction for Auth/Void Failed",
        "D4450": "Visa Checkout Transaction Error Failed"
    }


    def __init__(self, code, *args, **kwargs):
        if code not in TransactionError.INDEX.keys():
            raise ValueError('Invalid error code: {}'.format(code))

        super(TransactionError, self).__init__(code, TransactionError.INDEX[code], *args, **kwargs)