from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api = os.getenv("API_KEY")
id = os.getenv("PROJECT_ID")

# Initialize IBM Watson credentials
credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key=api,
)
client = APIClient(credentials)

# Define the Watson model
model = ModelInference(
    model_id="ibm/granite-13b-chat-v2",
    api_client=client,
    project_id=f"{id}",
    params={"max_new_tokens": 50},
)

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# User input
user_input = "I can help people"

# Construct the prompt for Watson
prompt = f"""
You are a matchmaker helping to assess messages in times of crisis. 
Read the following message and respond with words that match the tone.
Respond WITH ANGER if the user needs help. Response with positive intense
emotions if the user can help. Ask for clarification otherwise:

"{user_input}"
"""

# Get Watson's generated response
watson_response = model.generate_text(prompt)
print(f"Watson's response: {watson_response}")

# Analyze sentiment of each sentence individually
sentences = watson_response.split('. ')
compound_scores = [sentiment_analyzer.polarity_scores(sentence)['compound'] for sentence in sentences]

# Average compound score across sentences
average_score = sum(compound_scores) / len(compound_scores)

# Determine the intended response based on the sentiment
if average_score >= 0.05:
    intended_response = "Able to help"
elif average_score <= -0.05:
    intended_response = "Needs help"
else:
    intended_response = "No longer needs help or Cannot help"

# Print the sentiment and the intended response
print(f"Sentiment scores: {compound_scores}")
print(f"Average sentiment score: {average_score}")
print(f"Determined response: {intended_response}")
