'''
The module to contain implementations of the payment methods, which defined by the specification as follows:
 - Transparent Redirect
 - Direct Connection
 - Responsive Shared Page
 - Refunds
 - Token Payments
 - Recurring Payments
'''


from eway.rapid.exception import EwayError


class Method(object):
    '''
    Abstract payment method class with commont methods for all the payment method implementations
    '''
    _client = None

    def __init__(self, client):
        '''
        Initializes the object

        Parameters:
            client : .client.Client = Initialised client
        '''

        self._client = client

    def trigger_errors(self, codes, *args, **kwargs):
        '''
        Raise exceptions accordingly to the codes passed

        Arguments:
            codes     : [str]    = List of error codes to be processed
            * args    : [?]      = Additional arguments to be passed to exception constructors
            ** kwargs : {str: ?} = Additional arguments to be passed to exception constructors
        '''
        for code in codes:
            error = EwayError.lookup_error_by_code(code, *args, **kwargs)

            if error:
                raise error
