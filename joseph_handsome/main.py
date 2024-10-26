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
      "max_new_tokens": 8000
  }
)

prompt = """You are a hurricane helper and a CSV data generator. Your task is to respond exclusively with a CSV-formatted table that includes real, unique data from the CSV file provided.

When prompted, respond with a CSV table containing exactly 5 hospitals based on the user’s input ZIP code location. Specifically, focus on hospitals that are geographically closest to the input ZIP code, 34744, located in the Orlando area.

Use only relevant columns for a quick, user-friendly display on a website. Prioritize hospitals in the same city or within approximately a 10-mile radius. If this information isn't directly available in the CSV, assume locations with ZIP codes starting with '328' or '347' as closer options and avoid results from distant cities, like Jacksonville or Gainesville.

Here is the format of the CSV response:
Hospital Name, Address, Phone Number, Distance (miles)

Ensure:
1. The data is from the provided CSV file only.
2. All phone numbers and addresses are unique.
3. The CSV should not include any extraneous text or headers; the output should strictly match the CSV format, which allows easy integration into a website table.
4. The tone should be helpful, but the response itself should only contain data, with no explanations or additional messages. Make sure the distance includes units in miles.

Generate a CSV of the 5 closest hospital facilities near ZIP code 33019 (Hialeah) using the information provided in the CSV file."""

#print(model.generate(prompt))
print(model.generate_text(prompt))
