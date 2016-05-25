# eway-rapid-python
Python client implementation for eWAY Rapid API v3

# Installation

```bash
pip install eway-rapid-python
```

# API parts implementation status:

```
  + = Implemented
  - = To be implemented in future versions
```

 * + `Transparent Redirect`
 * - `Direct Connection`
 * - `Responsive Shared Page`
 * - `Refunds`
 * - `Transaction Query`
 * - `Pre-Auth`
 * - `Token Payments`
 * - `Settlement Search`
 * - `Recurring Payments`
 


# Rapid API v3

Rapid API documentation: https://eway.io/api-v3

# Basic usage

```python
from eway.rapid.client import RestClient
from eway.rapid.endpoint import SandboxEndpoint
from eway.rapid.model import Payment, RequestMethod, TransactionType
from eway.rapid.payment_method.transparent_redirect import TransparentRedirect, CreateAccessCodeRequest

payment_method = TransparentRedirect(RestClient('api-key', 'api-password', SandboxEndpoint()))

# response is eway.rapid.payment_method.transparent_redirect.response.AccessCodeResponse
response = payment_method.create_access_code(CreateAccessCodeRequest(
    Payment(4200, 'AUD'),
    RequestMethod.ProcessPayment,
    TransactionType.Purchase,
    'https://localhost/'
))

print(response.to_json())

# ... here client performs form submit in his browser

# transaction is eway.rapid.payment_method.transparent_redirect.response.TransactionInfo
transaction = payment_method.request_transaction_result(response.AccessCode)

print(transaction.to_json())
```

For more complete example have a look at [Transparent Redirect tests](./tests/transparent_redirect.py)

# Testing

```bash
python -m unittest tests
```


# License

The MIT License (MIT). Please see [License File](LICENSE) for more information.
