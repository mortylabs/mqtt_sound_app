# 🚀 MQTT Sound App

This project listens for **MQTT messages** and plays **MP3 sound files** stored in a mounted directory.  
It supports playing up to **3 sequential sounds** per message.

## 🛠 Features
- ✅ **Subscribes to MQTT** for `home/automation/play_sound`
- ✅ **Plays MP3 files** from a **mounted directory**
- ✅ **Logs messages dynamically** based on `LOGGING_LEVEL`
- ✅ **Sends Telegram alerts** for missing files or errors
- ✅ **Runs in Docker** and supports **k3s deployments**

---

## 📥 **Installation (Without Docker)**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/mortylabs/mqtt_sound_app.git
   cd mqtt_sound_app

2. **Set up Python environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your values

6. **Run the script:**
   ```bash
   python mqtt_sound_app.py


## **🐳 Running with Docker**
1. **Build the Docker image:**
   ```bash
   docker build -t mqtt-sound-app .

2. **Run the container:**
   ```bash
   docker run -d --name mqtt_sound_app \
   --env-file .env \
   -v /home/pi/Music:/music:ro \
   mortyone/mqtt-sound-app

## 🚀 **Deploying to k3s**

1. see [mortylabs/kubernetes](https://github.com/mortylabs/kubernetes) for k3s deployment.yaml
