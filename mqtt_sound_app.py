#!/usr/bin/python3
import os
import subprocess
import logging
import json
import requests
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment Variables
MQTT_BROKER = os.getenv("MQTT_SERVER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DIR_MUSIC = os.getenv("DIR_MUSIC", "/music")  # Mounted music directory

# Set Logging Level from Environment Variable
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

logging.basicConfig(level=LOG_LEVELS.get(LOGGING_LEVEL, logging.INFO), format="%(asctime)s %(levelname)s: %(message)s")


def send_telegram_alert(message):
    """ Sends a Telegram notification. """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning("Telegram bot token or chat ID not set, skipping alert.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    
    try:
        requests.post(url, json=payload)
    except requests.exceptions.RequestException as e:
        logging.error(f"Telegram message failed: {e}")

def play_sound(payload):
    """ Play up to 3 MP3 files sequentially from the mounted /music directory. """
    sound_files = [
        payload.get('file1'),
        payload.get('file2'),
        payload.get('file3')
    ]

    for sound_file in sound_files:
        if not sound_file:
            continue  # Skip empty file entries

        file_path = os.path.join(DIR_MUSIC, sound_file)

        if not os.path.isfile(file_path):
            logging.warning(f"⚠ MP3 missing: {file_path}")
            send_telegram_alert(f"⚠ MP3 missing: {file_path}")
            continue  # Skip missing files

        try:
            logging.info(f"▶ Playing {file_path}")
            subprocess.run(["mplayer", file_path], check=True)
        except Exception as e:
            logging.error(f"❌ Failed to play {file_path}: {e}")
            send_telegram_alert(f"❌ Failed to play {file_path}: {e}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        logging.info(f"Message received: {msg.topic} -> {payload}")

        actions = {
            'home/automation/play_sound': play_sound,
        }

        action = actions.get(msg.topic)
        if action:
            action(payload)

    except Exception as e:
        send_telegram_alert(f"Error processing MQTT message: {e}")

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)

    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.subscribe([("home/automation/play_sound", 0)])
        logging.info("MQTT Listener Started")
        client.loop_forever()
    except Exception as e:
        send_telegram_alert(f"MQTT connection error: {e}")

if __name__ == "__main__":
    main()
