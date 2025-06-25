# Seilkamera

Dieses Projekt wurde von **Amadeo Püchner** und **Janik Loibenegger** im Rahmen des Physikunterrichts am Gymnasium Schillerstraße in Feldkirch bei **Winfried Brüser** entwickelt. Ziel war es, eine seilgeführte Kamera zu bauen, die sich mithilfe von vier Motoren präzise durch einen Raum bewegen lässt.

---

## 🔧 Funktionen

* Steuerung von vier Schrittmotoren über Raspberry Pi
* Webinterface zur manuellen Steuerung
* Vordefinierte Bewegungsmuster (Presets)
* Geschwindigkeit einstellbar über Weboberfläche
* Hardware-Simulation auf Nicht-Raspberry-Geräten möglich

---

## 📁 Projektstruktur

```
├── __main__.py               # Einstiegspunkt
├── server.py                 # Flask Webserver + Socket.IO
├── motor_control.py          # Einzelschrittmotorsteuerung
├── preset_runner.py          # Ausführen von Presets (Bewegungsabläufe)
├── fake_gpio.py              # GPIO-Ersatz für Nicht-RPi-Systeme
├── stop.py                   # GPIO-Pins sicher zurücksetzen
├── pins.json                 # Pinbelegung für Motoren A–D
├── presets.json              # Vordefinierte Presets
├── speed.txt                 # Aktuelle Bewegungsgeschwindigkeit
├── templates/
│   ├── index.html            # Hauptsteuerungsseite
│   └── settings.html         # Konfigurationsoberfläche
```

---

## ⚙️ Voraussetzungen

### Raspberry Pi:

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask flask-socketio RPi.GPIO
```

### Alternativ (für Tests ohne GPIO):

```bash
pip3 install flask flask-socketio
```

---

## 🚀 Start

```bash
python3 __main__.py
```

Dann im Browser aufrufen:

```
http://<IP_DES_PI>:5000
```

---

## 📷 Anwendung

* Positioniere die Kamera an vier Seilen, die über die Motoren gespannt werden.
* Starte den Webserver auf dem Raspberry Pi.
* Greife per Webbrowser auf die Oberfläche zu.
* Steuere manuell oder starte voreingestellte Bewegungsmuster.

---

## 📌 Hinweis

Dieses Projekt ist rein schulischer Natur und dient Demonstrations- und Lernzwecken. Fehler oder Verbesserungsvorschläge sind willkommen!
