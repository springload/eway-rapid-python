from eway.rapid.exception import EwayError


class Method(object):
    _client = None


    def __init__(self, client):
        '''
        Initializes the object

        Parameters:
            client : .client.Client = Initialised client
        '''

        self._client = client


    def trigger_errors(self, codes, **kwargs):
        for code in codes:
            error = EwayError.lookup_error_by_code(code, **kwargs)

            if error:
                raise error