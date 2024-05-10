const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const wwebVersion = process.env.WHATSAPP_WEB_VERSION || "2.2412.54";

// Fix for the WhatsApp Web version bug, was taken from the official repository as a fix to a local cache bug
const WWJS_BUG_URL_FIX = `https://raw.githubusercontent.com/wppconnect-team/wa-version/main/html/${wwebVersion}.html`;

async function scrape_whatsapp_chat(msg_handler, chat_id) {
  if (typeof chat_id !== "string") {
    console.error("chat_id must be a string");
    return -1;
  }

  if (typeof msg_handler !== "function") {
    console.error("msg_handler must be a function");
    return -1;
  }

  const client = new Client({
    authStrategy: new LocalAuth(),
    webVersionCache: {
      type: "remote",
      remotePath: WWJS_BUG_URL_FIX,
    },
    puppeteer : {
      headless: true,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--no-first-run",
        "--no-zygote",
        "--single-process", 
        "--disable-gpu",
      ],
    }
  });

  client.on("qr", (qr) => {
    console.log("QR Code generated, scan please:");
    qrcode.generate(qr, { small: true });
  });

  client.on("ready", () => {
    console.log("WhatsApp client is ready!");
  });

  client.on("message", async (msg) => {
    if (msg.from === chat_id) {
      try {
        await msg_handler(msg);
      } catch (error) {
        console.error("Error handling message:", error);
      }
    }
  });

  client.on('auth_failure', message => {
    console.error('Authentication failure:', message);
  });

  client.on('disconnected', (reason) => {
    console.log('Client was disconnected:', reason);
  });

  client.initialize();

  process.on('SIGINT', () => {
    client.destroy().then(() => {
        console.log('Client closed');
        process.exit(0);
    });
  });
}

module.exports = { scrape_whatsapp_chat };
