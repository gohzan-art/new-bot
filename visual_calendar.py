import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import io

class VisualCalendar:
    def __init__(self):
        self.calendar_api = GoogleCalendarAPI()

    async def generate_calendar_image(self, start_date, end_date):
        events = await self.calendar_api.list_events({"start": start_date, "end": end_date})
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_title("Visual Calendar")
        
        # Set up the x-axis with dates
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        ax.set_xlim([start, end])
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        # Plot events
        for event in events:
            event_start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
            event_end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
            ax.axvspan(event_start, event_end, alpha=0.3)
            ax.text(event_start, 0, event['summary'], rotation=90, verticalalignment='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        
        return buf