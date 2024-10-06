from openai import OpenAI
import os
from dotenv import load_dotenv
import spacy
import dateparser
from datetime import datetime, timedelta
import pytz

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.timezone = pytz.timezone('America/El_Paso')
        self.name = "SGT Dickburgler"

    def get_current_time(self):
        return datetime.now(self.timezone)

    def identify_intent(self, query):
        current_time = self.get_current_time()
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": f"You are {self.name}, a military calendar assistant. The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}. Identify the intent of the following calendar-related query."},
                {"role": "user", "content": query}
            ]
        )
        intent = response.choices[0].message.content.strip().lower()
        return intent

    def extract_event_details(self, query):
        current_time = self.get_current_time()
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": f"You are {self.name}, a military calendar assistant. The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}. Extract event details from the following query. Provide a JSON response with keys: summary, start, end, location."},
                {"role": "user", "content": query}
            ]
        )
        event_details = eval(response.choices[0].message.content)
        return event_details

    def parse_date_time(self, date_string):
        return dateparser.parse(date_string, settings={'PREFER_DATES_FROM': 'future', 'TIMEZONE': 'America/El_Paso', 'RETURN_AS_TIMEZONE_AWARE': True})

    def extract_time_range(self, query):
        current_time = self.get_current_time()
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": f"You are {self.name}, a military calendar assistant. The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}. Extract the time range from the following query. Provide a JSON response with keys: start, end."},
                {"role": "user", "content": query}
            ]
        )
        time_range = eval(response.choices[0].message.content)
        return time_range

    def generate_response(self, action, details):
        current_time = self.get_current_time()
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": f"You are {self.name}, a military calendar assistant. The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}. Generate a natural language response for a calendar action. Action: {action}, Details: {details}"},
                {"role": "user", "content": "Generate response"}
            ]
        )
        return response.choices[0].message.content.strip()