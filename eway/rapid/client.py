import requests

from logging import Logger, getLogger
from requests.exceptions import ConnectionError

from .endpoint import Endpoint
from .exception import ResponseError




class Client(object):
    '''
    Client for eWAY Rapid API v3
    '''

    _api_key = ''

    _api_password = ''

    _endpoint = None

    _logger = None


    def __init__(self, api_key, api_password, endpoint, logger=None):
        '''
        Initializes the client.

        Parameters:
            api_key        : str                 = eWAY API Key
            api_password   : str                 = eWAY API Password
            endpoint       : .endpoint.Endpoint  = Initialised endpoint
            logger         : logging.Logger      = default value is `logging.getLogger('eway.rapid.client')`
        '''

        if not logger:
            logger = getLogger('eway.rapid.client')

        self._logger = logger

        self._validate_credentials(api_key, api_password)
        self._api_key = api_key
        self._api_password = api_password

        self._validate_endpoint(endpoint)
        self._endpoint = endpoint


    def _validate_credentials(self, api_key, api_password):
        if not len(api_key) or not len(api_password):
            self._logger.error('API key and password are invalid')
            raise ResponseError('S9991') # Rapid API key or password not set


    def _validate_endpoint(self, endpoint):
        if not len(endpoint.get_url()):
            self._logger.error('Endpoint returns empty URL')
            raise ResponseError('S9990') # Rapid endpoint not set or invalid

        # TODO: do we have any more appropriate pong methods on the API side?
        # try:
        #     requests.head(endpoint.get_url())
        # except ConnectionError:
        #     self._logger.critical('ConnectionError to the endpoint {}'.format(endpoint.get_url()))
        #     raise InvalidEndpointError()

    def transparent_redirect_create_access_code(self, request):
        raise TypeError('Method transparent_redirect_create_access_code has not been implemented')


    def transparent_redirect_get_transaction_info(self, access_code):
        raise TypeError('Method transparent_redirect_get_transaction_info has not been implemented')



class RestClient(Client):
    def transparent_redirect_create_access_code(self, request):
        '''
        TransparentRedirect STEP 1

        Pass the customer and transaction details to eWAY to generate an Access Code

        Arguments:
            request : .payment_method.TransparentRedirect.CreateAccessCodeRequest
        '''
        url = '{}{}'.format(self._endpoint.get_url(), 'AccessCodes')

        json_string = request.to_json()

        response = requests.post(url, auth=(self._api_key, self._api_password), data=json_string, headers={'Content-Type': 'application/json'})

        return self._validate_response(response)



    def transparent_redirect_get_transaction_info(self, access_code):
        '''
        TransparentRedirect STEP 3

        Once the transaction has been processed, request the results from eWAY using the Access Code

        WARNING: An Access Code can only be queried for one week after it has been created

        Arguments:
            access_code : str(512) = The Access Code
        '''
        url = '{}{}/{}'.format(self._endpoint.get_url(), 'AccessCode', access_code)

        response = requests.get(url, auth=(self._api_key, self._api_password))

        return self._validate_response(response)



    def _validate_response(self, response):
        txt = response.text.strip()

        if response.status_code == 401:
            raise ResponseError('S9993') # Authentication error

        elif response.status_code == 404:
            raise ResponseError('S9990') # Rapid endpoint not set or invalid

        elif response.status_code >= 500:
            raise ResponseError('S9996') # Rapid gateway server error

        elif len(txt) == 0:
            raise ResponseError('S9902') # Empty response

        elif not txt.startswith(u'{') or not txt.strip().endswith(u'}'):
            raise ResponseError('S9901') # Response is not JSON

        return txt