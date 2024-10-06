const natural = require('natural');
const chrono = require('chrono-node');

class NLPProcessor {
  constructor() {
    this.tokenizer = new natural.WordTokenizer();
  }

  identifyIntent(query) {
    const tokens = this.tokenizer.tokenize(query.toLowerCase());
    if (tokens.some(token => ['create', 'add', 'schedule', 'new'].includes(token))) return 'create';
    if (tokens.some(token => ['list', 'show', 'display', 'what', 'when'].includes(token))) return 'list';
    if (tokens.some(token => ['update', 'change', 'modify', 'reschedule'].includes(token))) return 'update';
    if (tokens.some(token => ['delete', 'remove', 'cancel'].includes(token))) return 'delete';
    return 'unknown';
  }

  extractEventDetails(query) {
    const parsedDate = chrono.parse(query);
    let startTime, endTime;
    if (parsedDate.length > 0) {
      startTime = parsedDate[0].start.date();
      endTime = parsedDate[0].end ? parsedDate[0].end.date() : new Date(startTime.getTime() + 60 * 60 * 1000);
    }

    return {
      summary: this.extractEventName(query),
      start: { dateTime: startTime ? startTime.toISOString() : null },
      end: { dateTime: endTime ? endTime.toISOString() : null },
    };
  }

  extractTimeRange(query) {
    const parsedDate = chrono.parse(query);
    let startTime = new Date();
    let endTime = new Date(startTime.getTime() + 7 * 24 * 60 * 60 * 1000);

    if (parsedDate.length > 0) {
      startTime = parsedDate[0].start.date();
      endTime = parsedDate[0].end ? parsedDate[0].end.date() : new Date(startTime.getTime() + 7 * 24 * 60 * 60 * 1000);
    }

    return {
      start: startTime.toISOString(),
      end: endTime.toISOString(),
    };
  }

  extractEventUpdates(query) {
    // This is a simplified version. You might want to make it more robust.
    const eventId = this.extractEventName(query);
    const parsedDate = chrono.parse(query);
    const updates = {};

    if (parsedDate.length > 0) {
      updates.start = { dateTime: parsedDate[0].start.date().toISOString() };
      updates.end = { dateTime: parsedDate[0].end ? parsedDate[0].end.date().toISOString() : new Date(parsedDate[0].start.date().getTime() + 60 * 60 * 1000).toISOString() };
    }

    return { eventId, updates };
  }

  extractEventId(query) {
    // This is a simplified version. You might want to make it more robust.
    return this.extractEventName(query);
  }

  extractEventName(query) {
    // This is a very basic implementation. You might want to improve it.
    const tokens = this.tokenizer.tokenize(query);
    return tokens.slice(0, 3).join(' '); // Just use the first three words as the event name
  }
}

module.exports = NLPProcessor;