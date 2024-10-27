import imaplib2
import email
from email.header import decode_header
from .models import EmailLog
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

def fetch_and_log_emails():
    IMAP_SERVER = 'imap.gmail.com'
    EMAIL_ACCOUNT = 'your-email@example.com'
    PASSWORD = 'your-password'

    mail = imaplib2.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')

    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        parsed_email = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(parsed_email['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')

        email_address = parsed_email['From']
        body = ""

        if parsed_email.is_multipart():
            for part in parsed_email.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = parsed_email.get_payload(decode=True).decode()
        
        body = body_translate(body)

        EmailLog.objects.create(email_address=email_address, email_body=body)

    mail.logout()

def body_translate():

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

    return intended_response
