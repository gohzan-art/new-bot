const { google } = require('googleapis');
const fs = require('fs');

class GoogleCalendarAPI {
  constructor() {
    this.auth = this.getAuth();
    this.calendar = google.calendar({ version: 'v3', auth: this.auth });
  }

  getAuth() {
    const credentials = JSON.parse(fs.readFileSync('credentials.json'));
    return new google.auth.JWT(
      credentials.client_email,
      null,
      credentials.private_key,
      ['https://www.googleapis.com/auth/calendar']
    );
  }

  async createEvent(eventDetails) {
    const response = await this.calendar.events.insert({
      calendarId: 'primary',
      resource: eventDetails,
    });
    return response.data;
  }

  async listEvents(timeRange) {
    const response = await this.calendar.events.list({
      calendarId: 'primary',
      timeMin: timeRange.start,
      timeMax: timeRange.end,
      singleEvents: true,
      orderBy: 'startTime',
    });
    return response.data.items;
  }

  async updateEvent(eventId, updates) {
    const response = await this.calendar.events.patch({
      calendarId: 'primary',
      eventId: eventId,
      resource: updates,
    });
    return response.data;
  }

  async deleteEvent(eventId) {
    await this.calendar.events.delete({
      calendarId: 'primary',
      eventId: eventId,
    });
  }
}

module.exports = GoogleCalendarAPI;