from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from dotenv import load_dotenv

load_dotenv()

def w_str_str(user_input):
    api_key = os.getenv('WATSON_KEY')
    service_url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com'
    
    # Set up authenticator and Watson service instance
    authenticator = IAMAuthenticator(api_key)
    assistant = AssistantV2(
        version='2021-06-14',
        authenticator=authenticator
    )
    assistant.set_service_url(service_url)

    # Define a session (optional, depending on the API version)
    session_id = assistant.create_session(
        assistant_id='your-assistant-id'
    ).get_result()['session_id']

    response = assistant.message(
        assistant_id='your-assistant-id',
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': user_input
        }
    ).get_result()
    return response['output']['generic'][0]['text']

# Test the function
user_input = "Hello, Watson!"
response_text = w_str_str(user_input)
print("Watson's Response:", response_text)
