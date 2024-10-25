# https://tessadem.com/elevation-api/
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Replace with your Watson API key and endpoint
api_key = 'your-api-key'
service_url = 'your-service-url'

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

# Function to get response from Watson API
def watson_api_call(user_input):
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
response_text = watson_api_call(user_input)
print("Watson's Response:", response_text)
