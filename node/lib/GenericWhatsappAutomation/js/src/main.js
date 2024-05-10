const { scrape_whatsapp_chat } = require('./whatsapp_manager.js'); // Import the scraper function
const { loadJsonFile } = require('./db_handler.js'); // Make sure the path matches where your function is defined
const CONFIG_FILE_PATH = "config/config.json"; // Path to the configuration file

// Example message handler function
async function handleMessage(message) {
  console.log("Received message:", message.body);
}

// Main function to setup the WhatsApp scraper
async function main() {
  try {
    const config = await loadJsonFile(CONFIG_FILE_PATH); // Load configuration from a JSON file
    if (config && config.chat_id) {
      await scrape_whatsapp_chat(handleMessage, config.chat_id);
    } else {
      console.error("Configuration file is missing 'chat_id'");
    }
  } catch (error) {
    console.error('Failed to load configuration or initialize WhatsApp scraper:', error);
  }
}

main().catch(console.error);
