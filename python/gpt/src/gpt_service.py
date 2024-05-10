from flask import Flask, request, jsonify
from openai import OpenAI, APIError

import json
import datetime
import requests

app = Flask(__name__)

# Function to load the OpenAI API key from a JSON file
def load_api_key():
    try:
        with open('keys/open_ai.json', 'r') as file:
            data = json.load(file)
            return data['key']
    except Exception as e:
        print(f"Failed to load API key: {e}")
        return None

# Load the OpenAI API key
OPENAI_API_KEY = load_api_key()

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Endpoint to handle incoming messages from WhatsApp
@app.route('/whatsapp', methods=['POST'])
def handle_message():
    # Extract message text from the incoming JSON data
    data = request.get_json()
    message_text = data['message']
    
    # Print the incoming message text
    print(message_text)

    try:
        # Get today's date in DD/MM/YYYY format
        today_date = datetime.datetime.today().strftime('%d/%m/%Y')
        # Get today's day of the week
        today_day = datetime.datetime.today().strftime('%A')
        print(today_date)
        
        # Send the message to the OpenAI API for processing
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": f"If the following message is an event."\
                   "Summarize the time (%H:%M:%S), date and event summary in the following format:\nyes\n{\"summary\":\"SUMMARY\", \"date\":DATE, \"time\":TIME}\n\notherwise, return\nno."},
                {"role": "user", "content": message_text}
            ]
        )

        # Get the OpenAI response
        output = completion.choices[0].message.content
        
        # Print the OpenAI response
        print(output)

        # If the OpenAI response indicates that it's an event
        if output.startswith("yes"):
            # URL of the calendar service to add the event
            calendar_service_url = 'http://calendar-service:5544/add_event'
            # Split the output into event details
            event_details = output.split('\n')[1:]
            # Convert the event details string to a dictionary
            dict_output = json.loads(event_details[0])
            # Send a follow-up message to get the correct date format
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": f"today's date (DD/MM/YYYY) is {today_date}, today's day is {today_day}. Answer date only as %Y-%m-%d"},
                    {"role": "user", "content": f"What date is {dict_output['date']}?"}
                ]
            )
            # Get the response to the follow-up message
            output = completion.choices[0].message.content
            print(f"{dict_output['date']} is {output}")
            # Update the date format in the event details dictionary
            dict_output['date'] = output
            # Send a POST request to the calendar service to add the event
            requests.post(calendar_service_url, json={"details": dict_output})
            return jsonify({"status": "event added"}), 200
        else:
            # If it's not an event, return a JSON response indicating so
            return jsonify({"status": "no event"}), 200

    except APIError as e:
        # If there's an API error, return an error response
        return jsonify({"error": "Failed to communicate with OpenAI", "message": str(e)}), 500

if __name__ == '__main__':
    # Start the Flask application with debug mode enabled on port 5500
    app.run(host="0.0.0.0", debug=True, port=5500)
