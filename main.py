from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url = "https://{region}.ml.cloud.ibm.com",
    api_key = "{apikey}",
)

client = APIClient(credentials)
