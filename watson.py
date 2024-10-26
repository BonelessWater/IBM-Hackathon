import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

# Load environment variables from .env
load_dotenv()

# Watson NLU API credentials
NLU_API_KEY = os.getenv('NLU_API_KEY')
NLU_URL = os.getenv('NLU_URL')

# Initialize Watson NLU client
authenticator = IAMAuthenticator(NLU_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version='2023-10-25',
    authenticator=authenticator
)
nlu.set_service_url(NLU_URL)

def get_hurricane_news():
    """Scrape weather-related news articles about hurricanes."""
    url = "https://weather.com/news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve news: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', class_='ArticleTile--title--3YFuh')
    news_urls = []

    for article in articles[:5]:  # Limit to 5 articles
        link = article.get('href')
        if link:
            news_urls.append(f"https://weather.com{link}")

    return news_urls

def analyze_article(url):
    """Analyze the entities and keywords of a hurricane-related article."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve article: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = " ".join([p.get_text() for p in paragraphs])

    # Analyze entities and keywords using Watson NLU
    analysis = nlu.analyze(
        text=article_text,
        features=Features(
            entities=EntitiesOptions(),
            keywords=KeywordsOptions()
        )
    ).get_result()

    return analysis

def extract_critical_info(analysis):
    """Extract key entities and keywords from the analysis."""
    entities = [entity['text'] for entity in analysis.get('entities', [])]
    keywords = [keyword['text'] for keyword in analysis.get('keywords', [])]

    print(f"Identified Entities: {entities}")
    print(f"Relevant Keywords: {keywords}")

    # Provide safety advice based on identified keywords/entities
    if any(word in keywords for word in ["evacuation", "shelter", "flood"]):
        print("⚠️ Important: Follow evacuation orders and find the nearest shelter.")
    if any(word in keywords for word in ["road closure", "blocked", "traffic"]):
        print("🚧 Warning: Some routes may be blocked. Check traffic updates.")
    if any(word in entities for word in ["food", "water", "supplies"]):
        print("🆘 Resources: Supplies are available. Head to the nearest aid station.")

def main():
    """Main function to scrape news and provide safety insights."""
    news_urls = get_hurricane_news()
    if not news_urls:
        print("No hurricane news articles found.")
        return

    print("Analyzing hurricane-related articles...")
    for url in news_urls:
        print(f"Analyzing: {url}")
        analysis = analyze_article(url)
        if analysis:
            extract_critical_info(analysis)
            print("-" * 40)


main()
