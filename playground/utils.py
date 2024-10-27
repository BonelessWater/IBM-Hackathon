from ibm_watsonx_ai.client import ibm_watsonx_ai
import imaplib2
import email
from email.header import decode_header
from .models import User
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

import logging
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_emails():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  user_id = 'me'
  query = 'is:unread'
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId=user_id, q=query).execute()
    messages = results.get("messages", [])

    if not messages:
      return {}
    parsed_messages = {}
    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id).execute()
        msg_subject = None
        msg_from = None
        
        for header in msg_data['payload']['headers']:
            if header['name'] == 'Subject':
                msg_subject = header['value']
            if header['name'] == 'From':
                msg_from = str(header['value'])
                msg_from = msg_from[msg_from.find("<")+1:-1]
                
        #print(f'{msg_from}')
        #print(f'{msg_subject}')
        parsed_messages[msg_from] = msg_subject
        #print('---')


        # Modify the message to remove the UNREAD label
        service.users().messages().modify(
            userId=user_id,
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

    return parsed_messages

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")
    return {}

def fetch_and_log_emails():
    msgs = get_emails()

    for key, value in msgs.items():
        logger.info(key+":"+value)
        print("-------------------------------")
        print(key+":"+value)
        print("-------------------------------")
        try:
            # Lookup the user profile based on the email
            user_profile = User.objects.get(email=key)
            
            # Update the state
            user_profile.state = body_translate(value)
            
            # Save the changes to the database
            user_profile.save()
            
            print(f"Updated state for {key} to {body_translate(value)}.")
        except ObjectDoesNotExist:
            print(f"No user found with email: {key}.")

def body_translate(user_input):

    # Load environment variables
    load_dotenv()

    api = os.getenv("API_KEY")
    id = os.getenv("PROJECT_ID")

    # Initialize IBM Watson credentials
    credentials = ibm_watsonx_ai.Credentials(
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

    # Construct the prompt for Watson
    prompt = f"""
    You are a matchmaker helping to assess messages in times of crisis. 
    Read the following message and respond with words that match the tone.
    Respond WITH ANGER if the user needs help. Response with positive intense
    emotions if the user can help. Ask for clarification otherwise:

    Here is the user's input: "{user_input}"

    Respond as instructed.
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
        intended_response = "helper"
    elif average_score <= -0.05:
        intended_response = "help"
    else:
        intended_response = "neither"

    # Print the sentiment and the intended response
    print(f"Sentiment scores: {compound_scores}")
    print(f"Average sentiment score: {average_score}")
    print(f"Determined response: {intended_response}")

    return intended_response
