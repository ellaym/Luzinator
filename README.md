# Luzinator Project Overview

The goal of this project is to automatically scrape WhatsApp chats and add relevant events directly to your calendar. It integrates Node.js, Python Flask, and Docker to manage WhatsApp message handling, event scheduling via Google Calendar, and text processing using OpenAI's GPT models.

## Project Structure

- **Node.js**: Manages WhatsApp message scraping and forwarding.
- **Python Flask**: Hosts two services for managing calendar events and processing messages with GPT.
- **Docker**: Utilized to containerize and orchestrate all the components.

## Components

1. **WhatsApp Service** (`./node`)
   - `main.js`: Initializes the WhatsApp scraper and message handling.
   - `db_handler.js`: Manages reading configuration from JSON files.

2. **Calendar Service** (`./python/calendar`)
   - `calendar_service.py`: Flask app that interacts with Google Calendar to schedule events based on message analysis from the GPT service.

3. **GPT Service** (`./python/gpt`)
   - `gpt_service.py`: Flask app that processes incoming WhatsApp messages to identify if they describe events using OpenAI's GPT model.

4. **Docker Configuration**
   - `docker-compose.yml`: Defines and runs the multi-container Docker applications for all services.

## Setup Instructions

1. **Configuration**:
   - Update the `keys` directories in the respective service directories to reflect your specific environment settings, such as API keys and service endpoints.
   - Verify the paths in the `config.json` files for the Node.js service.
   - Ensure Google Calendar API credentials are correctly configured in the calendar service.

2. **Building and Running Services**:
   - Execute `docker-compose up --build` to build and start all the services as defined in `docker-compose.yml`.

3. **Operational Workflow**:
   - The Node.js service scrapes messages from WhatsApp and forwards them to the GPT service.
   - The GPT service analyzes each message to determine if it pertains to an event.
   - Identified events are sent to the Calendar service to be added to the calendar.

## Additional Information

- Ensure that all dependencies are installed as specified in the `package.json` and `requirements.txt` files for the Node.js and Python services, respectively.
- All services communicate over a Docker-defined bridge network, ensuring efficient internal connectivity.

This configuration enables a seamless process for automated event management from WhatsApp chats, leveraging cutting-edge AI technology and cloud services.
