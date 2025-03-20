# 🔊 MQTT Sound App – Offline Smart Alerts for Home Assistant  

## 🎯 Why This Script Exists
I run **Home Assistant** as part of my smart home security setup and needed a way to **broadcast security alerts** to speakers in different rooms around the house. Some examples:
- **"Carport gate opened"**
- **"Motion detected in the back garden"**
- **"Garage door opened"**
- **"Front doorbell rang"**

### This app ensures that **security notifications continue to work even when the internet goes down**, because:
- ✅ **Does NOT need internet** – All processing is done locally.
- ✅ **Plays pre-recorded MP3 alerts instantly** – No cloud API or TTS delays.
- ✅ **Can be installed on multiple Raspberry Pis around the house** – Each with its own speaker for redundancy.
- ✅ **Runs on any Raspberry Pi** – Uses very little power, especially a Zero 2W, making it ideal for UPS backup.

### **🌍 Real-World Use Case: Loadshedding in South Africa**
This app was developed for **use in South Africa**, where scheduled **loadshedding (rolling blackouts)** can leave homes **without power for several hours per day**. This often results in:
- ❌ **Internet Service Providers (ISPs) going down during extended power outages**  
- ❌ **Smart speakers (Google Nest / Alexa) becoming useless** unless powered by a UPS.
- ❌ **Missed security alerts** during critical times.


This app **solves all of that** by turning your spare **Raspberry Pis into local smart speakers** that play **instant, pre-recorded MP3 alerts** for your **security system**.  

### **🚀 Why It's Better**  
- ✅ **Works even if the internet is down.**  
- ✅ **Plays alerts instantly** – works locally, no cloud dependency, no TTS delays.  
- ✅ **Runs on any Raspberry Pi** – A **Zero 2W** is perfect for UPS backup.
- ✅ **Works in multiple rooms** – Just reuse another Pi with a speaker!  

## 📦 **Other Features**  
- ✅ **Deployable via Docker or Kubernetes (K3s).**  
- ✅ **Configurable via `.env` or Kubernetes Secrets.**  
- ✅ **Auto-detects available ALSA sound device inside the container.**  
- ✅ **Supports multiple MP3 files per message** (e.g., "door opened" + "alarm sound").
- ✅ **Configurable MQTT settings** via `.env` or Kubernetes Secrets.
- ✅ **Sends Telegram alerts** if a requested sound file is missing.
- ✅ **Auto-detects available ALSA sound device** inside the container.


---

## 🔥 **How It Works**  
1️⃣ **Home Assistant sends an MQTT message** when an event occurs (e.g., "Garage door opened").  
2️⃣ **This app listens for MQTT messages** and plays the corresponding MP3 file.  
3️⃣ **Multiple MP3 files per message are supported** – chain sounds dynamically.  
4️⃣ **If a sound file is missing, an alert is sent to Telegram.**  

💡 You can create your own MP3 alerts using any voice editor or text-to-speech (TTS) service, such as Google Cloud TTS, Amazon Polly, or local tools like Balabolka.

---


## ⚙️ **Configuration**  
You can configure MQTT Sound App using a `.env` file or Kubernetes Secrets.

### **📌 Environment Variables**  
| Variable              | Default Value                         | Description |
|-----------------------|-------------------------------------|-------------|
| `MQTT_BROKER`        | `192.168.1.10`                      | MQTT broker IP or hostname |
| `MQTT_PORT`          | `1883`                               | MQTT broker port |
| `MQTT_USER`          | *(empty)*                            | MQTT username (optional) |
| `MQTT_PASS`          | *(empty)*                            | MQTT password (optional) |
| `MQTT_TOPIC`         | `home/automation/play_sound`        | MQTT topic to listen on |
| `TELEGRAM_BOT_TOKEN` | *(empty)*                            | Telegram bot token for alerts |
| `TELEGRAM_CHAT_ID`   | *(empty)*                            | Telegram chat ID to send alerts |
| `DIR_MUSIC`          | `/music`                             | Directory where MP3 files are stored |
| `LOGGING_LEVEL`      | `INFO`                               | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

# 🛠 **Installation**  

## **📥 Option 1: Running Locally (without Docker or kubernetes)**  
**Clone the repository**  
   ```bash
      git clone https://github.com/mortylabs/mqtt_sound_app.git
      cd mqtt_sound_app
   ```

**Set up Python environment**
   ```bash
      python3 -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -r requirements.txt
   ```

**Configure environment variables:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your values
   ```

**📌 Example `.env` file**
```ini
MQTT_BROKER=192.168.1.15
MQTT_PORT=1883
MQTT_USER=myuser
MQTT_PASS=mypassword
MQTT_TOPIC=home/automation/play_sound
TELEGRAM_BOT_TOKEN=123456:ABCDEF-TelegramToken
TELEGRAM_CHAT_ID=-1001234567890
DIR_MUSIC=/home/pi/Music
LOGGING_LEVEL=DEBUG
```

**Run the script:**
   ```bash
   python mqtt_sound_app.py
```
---

## **🐳 Option 2: Running with Docker**
1. **Build the Docker image:**
   ```bash
   docker build -t mqtt-sound-app .
   ```

2. **Run the container:**
   ```bash
   docker run -d --name mqtt_sound_app \
   --env-file .env \
   -v /home/pi/Music:/music:ro \
   mortyone/mqtt-sound-app
   ```

## 🚀 **Deploying to k3s**

1. see [mortylabs/kubernetes](https://github.com/mortylabs/kubernetes) for k3s deployment.yaml
