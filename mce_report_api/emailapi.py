
# Python SDK: https://github.com/sendinblue/APIv3-python-library
from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

# create an instance of the API class
api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
create_contact = sib_api_v3_sdk.CreateContact(
  email= "wael.rashwan@tudublin.ie", 
) # CreateContact | Values to create a contact

try:
    # Create a contact
    api_response = api_instance.create_contact(create_contact)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->create_contact: %s\n" % e)
