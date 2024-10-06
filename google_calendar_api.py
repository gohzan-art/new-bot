from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarAPI:
    def __init__(self):
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        credentials = service_account.Credentials.from_service_account_file(
            'service_account.json', scopes=SCOPES)
        return build('calendar', 'v3', credentials=credentials)

    async def create_event(self, event_details):
        event = self.service.events().insert(calendarId='primary', body=event_details).execute()
        return event

    async def list_events(self, time_range):
        events_result = self.service.events().list(calendarId='primary', timeMin=time_range['start'],
                                                   timeMax=time_range['end'], singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    async def update_event(self, event_id, updates):
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        for key, value in updates.items():
            event[key] = value
        updated_event = self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        return updated_event

    async def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()