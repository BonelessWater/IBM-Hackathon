import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key and Endpoint from environment variables
API_KEY = os.getenv("API_KEY")
SCORING_ENDPOINT = (
    "https://us-south.ml.cloud.ibm.com/ml/v1/deployments/tuning_short/"
    "text/generation_stream?version=2021-05-01"
)

def get_iam_token(api_key):
    """Generate a new IAM token using the API key."""
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=30)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            print("Error: IAM token not found in response.")
            print("Response JSON:", response.json())
        return token
    except requests.exceptions.RequestException as e:
        print(f"Error generating IAM token: {e}")
        return None

def query_llama_model(iam_token, input_text, retries=3):
    """Query the deployed Llama model with retry logic."""
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    payload = {"input": input_text}

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to query the model...")
            response = requests.post(SCORING_ENDPOINT, json=payload, headers=headers, timeout=60)
            print(f"Received response with status code: {response.status_code}")
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes
            print("Parsing response JSON...")
            return response.json()
        except requests.exceptions.Timeout:
            print("Request timed out. Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying
        except requests.exceptions.RequestException as e:
            print(f"Error querying model: {e}")
            break  # Exit on non-timeout errors
    return None

def main():
    # Step 1: Generate a valid IAM token
    print("Generating IAM token...")
    iam_token = get_iam_token(API_KEY)
    if not iam_token:
        print("Failed to retrieve IAM token.")
        return

    # Step 2: Send minimal input to the model
    input_text = input("Enter text input for the model: ").strip() or "Hello"
    print(f"Using input: {input_text}")

    # Step 3: Query the model and print the result
    print("Querying the model...")
    result = query_llama_model(iam_token, input_text)
    if result:
        print("Model Output:", json.dumps(result, indent=4))
    else:
        print("Failed to get a valid response from the model.")

if __name__ == "__main__":
    main()
