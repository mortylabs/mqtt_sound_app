#!/usr/bin/python3
import os
import time
import json
import logging
import paho.mqtt.client as mqtt
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MQTT Configuration (with default values)
MQTT_BROKER = os.getenv("MQTT_BROKER", "192.168.1.15")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "home/automation/play_sound")  # Now configurable

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Directory for MP3 files
DIR_MUSIC = os.getenv("DIR_MUSIC", "/music")

# Logging Configuration
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
logging.basicConfig(level=LOGGING_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")

# Set ALSA as the default audio driver (Prevents JACK errors)
os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "hw:0,0"
os.environ["MPG123_MODOUT"] = "alsa"

# MQTT Client Setup (Fixes Deprecation Warning)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

if MQTT_USER and MQTT_PASS:
    client.username_pw_set(MQTT_USER, MQTT_PASS)

def send_telegram_message(message):
    """ Send a message to Telegram """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.debug("Telegram notifications are disabled. Skipping message.")
        return  # Exit without sending anything

    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            subprocess.run(["curl", "-s", "-X", "POST", telegram_url, "-d", json.dumps(payload), "-H", "Content-Type: application/json"])
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")

def play_sound(payload):
    """ Play sound files based on MQTT message payload """
    files = [payload.get(f"file{i}") for i in range(1, 4) if payload.get(f"file{i}")]

    if not files:
        logging.warning("No valid sound file provided in MQTT message")
        return

    for sound_file in files:
        sound_path = os.path.join(DIR_MUSIC, sound_file)
        if os.path.exists(sound_path):
            logging.info(f"Playing sound: {sound_path}")
            try:
                subprocess.run(["mpg123", "-o", "alsa", "-a", "hw:0,0", sound_path], check=False)
            except Exception as e:
                logging.error(f"Error playing {sound_file}: {e}")
        else:
            logging.error(f"Sound file not found: {sound_path}")
            send_telegram_message(f"Error: Sound file '{sound_file}' not found.")

def on_connect(client, userdata, flags, reason_code, properties):
    """ Handle MQTT connection """
    if reason_code == 0:
        logging.info(f"Connected to MQTT Broker {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        logging.info(f"Subscribed to MQTT topic: {MQTT_TOPIC}")
    else:
        logging.error(f"Failed to connect to MQTT Broker: {reason_code}")

def on_message(client, userdata, msg):
    """ Handle incoming MQTT messages """
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        logging.info(f"MQTT Message Received on {msg.topic}: {payload}")
        play_sound(payload)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON received on {msg.topic}: {msg.payload} | Error: {e}")

def main():
    """ Main function to start MQTT listener """
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        logging.info("MQTT Listener Started. Waiting for messages...")
        while True:
            time.sleep(30)  # Prevent CPU overuse
    except Exception as e:
        logging.error(f"MQTT connection error: {e}")
        send_telegram_message(f"MQTT Sound App Error: {e}")

if __name__ == "__main__":
    main()
