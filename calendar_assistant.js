const GoogleCalendarAPI = require('./google_calendar_api');
const NLPProcessor = require('./nlp_processor');

class CalendarAssistant {
  constructor() {
    this.calendarAPI = new GoogleCalendarAPI();
    this.nlpProcessor = new NLPProcessor();
  }

  async processQuery(query) {
    const intent = this.nlpProcessor.identifyIntent(query);
    switch (intent) {
      case 'create':
        return await this.createEvent(query);
      case 'list':
        return await this.listEvents(query);
      case 'update':
        return await this.updateEvent(query);
      case 'delete':
        return await this.deleteEvent(query);
      default:
        return "I'm not sure what you want to do. Can you please rephrase?";
    }
  }

  async createEvent(query) {
    const eventDetails = this.nlpProcessor.extractEventDetails(query);
    const event = await this.calendarAPI.createEvent(eventDetails);
    return `Event created: ${event.summary} at ${event.start.dateTime}`;
  }

  async listEvents(query) {
    const timeRange = this.nlpProcessor.extractTimeRange(query);
    const events = await this.calendarAPI.listEvents(timeRange);
    return events.map(event => `${event.summary} at ${event.start.dateTime}`).join('\n');
  }

  async updateEvent(query) {
    const { eventId, updates } = this.nlpProcessor.extractEventUpdates(query);
    const updatedEvent = await this.calendarAPI.updateEvent(eventId, updates);
    return `Event updated: ${updatedEvent.summary} at ${updatedEvent.start.dateTime}`;
  }

  async deleteEvent(query) {
    const eventId = this.nlpProcessor.extractEventId(query);
    await this.calendarAPI.deleteEvent(eventId);
    return "Event deleted successfully";
  }
}

module.exports = CalendarAssistant;