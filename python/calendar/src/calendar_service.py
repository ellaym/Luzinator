from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import datetime
import json

app = Flask(__name__)

# Paths to the service account key and configuration files
SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'keys/calendar_credentials.json')
CONFIG_FILE_PATH = "config/config.json"

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load configuration settings from a JSON file
def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return None

# Load the configuration and get the calendar ID
config = load_config()
if config:
    CALENDAR_ID = config.get("calendar_id", 'primary')

# Add an event to the Google Calendar
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json
    event_details = data.get('details', {})
    
    # Log the event date for debugging
    print(f"Event date: {event_details.get('date')}")

    # Initialize credentials and build the calendar service
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    # Prepare start and end datetime objects
    start_datetime = datetime.datetime.strptime(f'{event_details["date"]}T{event_details["time"]}', '%Y-%m-%dT%H:%M:%S')
    end_datetime = start_datetime + datetime.timedelta(hours=1)

    # Define the calendar event structure
    event = {
        'summary': event_details.get('summary', 'No Title'),
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Jerusalem',
        },
    }

    # Insert the event into the calendar
    event_response = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return jsonify({'status': 'success', 'event': event_response}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5544)
