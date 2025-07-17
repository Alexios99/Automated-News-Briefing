import requests
from datetime import date, timedelta
from difflib import SequenceMatcher
import os
import google.generativeai as genai
import urllib.parse
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer



GOOGLE_API_KEY = "AIzaSyAw6SKJKvOm_8t8F5nFhb1mR5frPJKfJRw" 
NEWS_API_KEY = '08e1a58d01f646b8aa2bf15e7e590ee0'      

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Error configuring Google AI: {e}")
    exit()



try:
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    chat = model.start_chat()
except Exception as e:
    print(f"Error initializing the Generative Model: {e}")
    exit()



# Define keywords for the query
keywords = [
    "green economy", "blue economy", "sustainable finance"
]
keywords2 =  ["Sustainable finance"]
QUERY = ' OR '.join([f'"{kw}"' for kw in keywords2])
encoded = urllib.parse.quote(QUERY)

# Define the date range for the query
FROM_DATE = (date.today() - timedelta(days=3)).isoformat()

# Construct the NewsAPI URL
url = ('https://newsapi.org/v2/everything?'
       f'q={encoded}&'
       f'from={FROM_DATE}&'
       'language=en&'
       'sortBy=publishedAt&'
       f'apiKey={NEWS_API_KEY}')

# Fetch articles from NewsAPI
response = requests.get(url)
data = response.json()

# Print the fetched articles
if data.get("status") == "ok":
    articles = data.get("articles", [])
    print(f"Fetched {len(articles)} articles:")
    for article in articles:
        print(f"- {article['title']} ({article['source']['name']})")
        print(article['content'])
        
else:
    print(f"Error fetching articles: {data.get('message', 'Unknown error')}")