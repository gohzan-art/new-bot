from openai import OpenAI
import os
from dotenv import load_dotenv
from google_calendar_api import GoogleCalendarAPI
from datetime import datetime, timedelta
import pytz

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class CalendarAssistant:
    def __init__(self):
        self.calendar_api = GoogleCalendarAPI()
        self.timezone = pytz.timezone('America/El_Paso')
        self.name = "SGT Dickburgler"

    async def process_query(self, query):
        current_time = datetime.now(self.timezone)
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": f"You are {self.name}, a military calendar assistant. The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}. Respond to the following calendar-related query:"},
                {"role": "user", "content": query}
            ]
        )
        
        ai_response = response.choices[0].message.content
        
        # Process the AI's response to extract action and details
        action, details = self._parse_ai_response(ai_response)

        # Perform the appropriate calendar action
        result = await self._perform_calendar_action(action, details)

        return f"{ai_response}\n\nAction taken: {result}"

    def _parse_ai_response(self, response):
        # This is a simplified parser. You might want to use more sophisticated NLP techniques here.
        lines = response.split('\n')
        action = None
        details = {}
        for line in lines:
            if "Action:" in line:
                action = line.split("Action:")[1].strip().lower()
            if "Event name:" in line:
                details['name'] = line.split("Event name:")[1].strip()
            if "Date:" in line:
                details['date'] = line.split("Date:")[1].strip()
            if "Time:" in line:
                details['time'] = line.split("Time:")[1].strip()
        return action, details

    async def _perform_calendar_action(self, action, details):
        # Implementation remains the same as before
        pass

    async def get_visual_calendar(self, start_date, end_date):
        events = await self.calendar_api.list_events({"start": start_date, "end": end_date})
        return self._generate_visual_calendar(events, start_date, end_date)

    def _generate_visual_calendar(self, events, start_date, end_date):
        # Implementation remains the same as before
        pass