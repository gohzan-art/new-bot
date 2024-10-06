import discord
from discord.ext import commands
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
from dotenv import load_dotenv
import spacy
import dateparser
from datetime import datetime, timedelta
import re
import pytz

load_dotenv()

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

class CalendarAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = get_calendar_service()
        self.timezone = pytz.timezone('America/New_York')  # Default timezone

    @commands.command()
    async def calendar(self, ctx, *, query: str):
        doc = nlp(query.lower())
        intent = self.identify_intent(doc)
        
        if intent == "create":
            await self.create_event(ctx, doc)
        elif intent == "list":
            await self.list_events(ctx, doc)
        elif intent == "delete":
            await self.delete_event(ctx, doc)
        elif intent == "update":
            await self.update_event(ctx, doc)
        else:
            await ctx.send("I'm not sure what you want to do with the calendar. Can you please rephrase?")

    def identify_intent(self, doc):
        create_keywords = ["create", "add", "schedule", "new"]
        list_keywords = ["list", "show", "display", "what", "when"]
        delete_keywords = ["delete", "remove", "cancel"]
        update_keywords = ["update", "change", "modify", "reschedule"]

        for token in doc:
            if token.text in create_keywords:
                return "create"
            elif token.text in list_keywords:
                return "list"
            elif token.text in delete_keywords:
                return "delete"
            elif token.text in update_keywords:
                return "update"
        return "unknown"

    async def create_event(self, ctx, doc):
        event_name = self.extract_event_name(doc)
        start_time, end_time = self.extract_time_range(doc)
        attendees = self.extract_attendees(doc)

        if not event_name:
            await ctx.send("I couldn't understand the event name. Can you please specify?")
            return
        if not start_time:
            await ctx.send("I couldn't understand the start time. Can you please specify?")
            return

        event = {
            'summary': event_name,
            'start': {'dateTime': start_time.isoformat(), 'timeZone': str(self.timezone)},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': str(self.timezone)},
        }

        if attendees:
            event['attendees'] = [{'email': attendee} for attendee in attendees]

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        await ctx.send(f'Event created: {event.get("htmlLink")}')

    async def list_events(self, ctx, doc):
        start_time, end_time = self.extract_time_range(doc)
        if not start_time:
            start_time = datetime.now(self.timezone)
        if not end_time:
            end_time = start_time + timedelta(days=7)  # Default to showing events for the next week

        events_result = self.service.events().list(calendarId='primary', timeMin=start_time.isoformat(),
                                                   timeMax=end_time.isoformat(), singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await ctx.send('No upcoming events found.')
        else:
            response = "Upcoming events:\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response += f"- {event['summary']} ({start})\n"
            await ctx.send(response)

    async def delete_event(self, ctx, doc):
        event_name = self.extract_event_name(doc)
        if not event_name:
            await ctx.send("I couldn't understand which event you want to delete. Can you please specify?")
            return

        events_result = self.service.events().list(calendarId='primary', q=event_name, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await ctx.send(f"No events found matching '{event_name}'.")
        elif len(events) > 1:
            await ctx.send(f"Multiple events found matching '{event_name}'. Please be more specific.")
        else:
            self.service.events().delete(calendarId='primary', eventId=events[0]['id']).execute()
            await ctx.send(f"Event '{event_name}' has been deleted.")

    async def update_event(self, ctx, doc):
        event_name = self.extract_event_name(doc)
        new_start_time, new_end_time = self.extract_time_range(doc)

        if not event_name:
            await ctx.send("I couldn't understand which event you want to update. Can you please specify?")
            return

        events_result = self.service.events().list(calendarId='primary', q=event_name, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await ctx.send(f"No events found matching '{event_name}'.")
        elif len(events) > 1:
            await ctx.send(f"Multiple events found matching '{event_name}'. Please be more specific.")
        else:
            event = events[0]
            if new_start_time:
                event['start']['dateTime'] = new_start_time.isoformat()
            if new_end_time:
                event['end']['dateTime'] = new_end_time.isoformat()

            updated_event = self.service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            await ctx.send(f"Event '{event_name}' has been updated: {updated_event.get('htmlLink')}")

    def extract_event_name(self, doc):
        # This is a simplified version. You might want to make it more robust.
        for ent in doc.ents:
            if ent.label_ == "EVENT":
                return ent.text
        return None

    def extract_time_range(self, doc):
        time_entities = [ent for ent in doc.ents if ent.label_ in ["TIME", "DATE"]]
        
        if len(time_entities) == 0:
            return None, None
        elif len(time_entities) == 1:
            start_time = dateparser.parse(time_entities[0].text, settings={'TIMEZONE': str(self.timezone)})
            end_time = start_time + timedelta(hours=1)  # Default to 1-hour events
        else:
            start_time = dateparser.parse(time_entities[0].text, settings={'TIMEZONE': str(self.timezone)})
            end_time = dateparser.parse(time_entities[1].text, settings={'TIMEZONE': str(self.timezone)})

        return start_time, end_time

    def extract_attendees(self, doc):
        # This is a very basic implementation. You might want to improve it.
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, doc.text)

def setup(bot):
    bot.add_cog(CalendarAssistant(bot))