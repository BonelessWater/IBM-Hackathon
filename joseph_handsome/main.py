from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from dotenv import load_dotenv
import os

load_dotenv()

api = os.getenv("API_KEY")
id = os.getenv("PROJECT_ID")


credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm.com",
    api_key = api,
)

client = APIClient(credentials)

model = ModelInference(
  model_id="ibm/granite-13b-chat-v2",
  api_client=client,
  project_id=f"{id}",
  params = {
      "max_new_tokens": 100
  }
)

prompt = 'How far is Paris from Bangalore?'
print(model.generate(prompt))
print(model.generate_text(prompt))
