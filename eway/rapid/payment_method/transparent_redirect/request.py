from eway.rapid.model import Payment, RequestMethod, StructMixin, TransactionType

class CreateAccessCodeRequest(StructMixin):
    '''
    Request for the Step1: CREATE A NEW ACCESS CODE

    Attributes:
        Method          : model.RequestMethod   = action to perform with this request
        TransactionType : model.TransactionType = type of transaction you're performing
        RedirectUrl     : str                   = web address the customer is redirected to with the result of the action

        Payment         : model.Payment         = (optional conditionally) details of the payment being processed,
                                                                           required when Method is ProcessPayment or TokenPayment
        Customer        : model.Customer        = (optional) details of the customer
        ShippingAddress : model.ShippingAddress = (optional) used by Beagle Fraud Alerts (Enterprise) to calculate a risk score for this transaction
        Items           : [model.Item]          = (optional) list of line items purchased by the customer (99 items maximum)
        Options         : [model.Option]        = (optional) not displayed to the customer but is returned in the result (99 options maximum)

        CustomerIP      : str                   = (optional) used by Beagle Fraud Alerts
        DeviceID        : str                   = (optional) identification name/number for the device or application
        PartnerID       : str                   = (optional) The partner ID generated from an eWAY partner agreement
        CheckoutPayment : bool                  = (optional) Setting this to "true" will process a PayPal Checkout payment
        CheckoutUrl     : str                   = (optional conditionally) when CheckoutPayment is set to "true" you must specify a CheckoutURL
                                                                           for the customer to be returned to after logging in to their PayPal account
    '''

    Method = None
    TransactionType = None
    RedirectUrl = ''
    Payment = None
    Customer = None
    ShippingAddress = None
    Items = []
    Options = []
    CustomerIP = None
    DeviceID = None
    PartnerID = None
    CheckoutPayment = None
    CheckoutUrl = None


    def __init__(self, payment, method, transaction_type, redirect_url, **kwargs):
        '''
        Makes a CreateAccessCodeRequest and sends it to eWAY

        Arguments:
            payment          : model.Payment         = (optional conditionally) details of the payment being processed,
                                                                                required when Method is ProcessPayment or TokenPayment
            method           : model.RequestMethod   = action to perform with this request
            transaction_type : model.TransactionType = type of transaction you're performing
            redirect_url     : str                   = web address the customer is redirected to with the result of the action
        '''
        super(CreateAccessCodeRequest, self).__init__(**kwargs)


        if not isinstance(method, RequestMethod):
            raise TypeError('method must be an instance of .model.RequestMethod')


        if not isinstance(transaction_type, TransactionType):
            raise TypeError('transaction_type must be an instance of .model.TransactionType')


        if not payment:
            payment = Payment()

        elif not isinstance(payment, Payment):
            raise TypeError('payment must be an instance of .model.Payment')


        self.Method = method
        self.TransactionType = transaction_type
        self.RedirectUrl = redirect_url
        self.Payment = payment