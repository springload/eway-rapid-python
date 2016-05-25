class Endpoint(object):
    '''
    Abstract

    eWAY Rapid API endpoint interface object.
    Exposes interface and should be inherited by all endpoint implementations.
    '''

    def get_url(self):
        'Returns URL address of the Rapid API endpoind'
        return self._url

    def is_sandbox(self):
        'Returns True if the endpoint is a sandbox'
        return False



class SandboxEndpoint(Endpoint):
    '''
    eWAY Rapid API sandbox endpoint implementation

    Attributes:
        _url    URL address of the Rapid API endpoind
    '''

    _url = r'https://api.sandbox.ewaypayments.com/'

    def is_sandbox(self):
        return True



class ProductionEndpoint(Endpoint):
    '''
    eWAY Rapid API production endpoint implementation

    Attributes:
        _url    URL address of the Rapid API endpoind
    '''
    
    _url = r'https://api.ewaypayments.com/'