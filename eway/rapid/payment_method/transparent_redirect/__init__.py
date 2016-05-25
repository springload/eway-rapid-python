from eway.rapid.payment_method import Method

from .request import CreateAccessCodeRequest
from .response import AccessCodeResponse, TransactionInfo


class TransparentRedirect(Method):
    def create_access_code(self, request):
        '''
        Makes a CreateAccessCodeRequest and sends it to eWAY

        Arguments:
            request : .request.CreateAccessCodeRequest = request to be performed
        '''

        response_json = self._client.transparent_redirect_create_access_code(request)

        ignore_unknown = False # TODO: True after lib stabilization
        response = AccessCodeResponse.from_json(response_json, ignore_unknown)

        if response.Errors:
            self.trigger_errors(response.Errors.split(','), response_struct=response, response_string=response_json)

        return response


    def request_transaction_result(self, access_code):
        '''
        Performs request of a transaction information by AccessCode
        '''

        response_json = self._client.transparent_redirect_get_transaction_info(access_code)

        ignore_unknown = False # TODO: True after lib stabilization
        response = TransactionInfo.from_json(response_json, ignore_unknown)

        if response.Errors:
            self.trigger_errors(response.Errors.split(','), response_struct=response, response_string=response_json)

        return response