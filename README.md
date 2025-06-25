# Internet of Things (IoT) Blinds Application System
A fully functional IoT solution for managing window blinds remotely. This project integrates ThingSpeak (MQTT and data channels) and Make.com for seamless automation via webhooks. Ideal for smart home setups and IoT experimentation.

---

## Introduction

The **Combination IoT Device** is a smart system built using MQTT, Python, ThingSpeak, and Make.com to simulate and manage automated window blinds. It publishes synthetic environmental data—**temperature**, **light (lux)**, and **sun position (radians)**—to platforms for visualization, control, and analysis.

ThingSpeak is used to visualize the data in real time, while Make.com logs data to Google Sheets and calculates blind positions. The results are pushed to `webhook.site` as raw JSON. A secondary Python script reads from ThingSpeak and generates a rolling temperature average in JSON, which is then visualized in a web environment using HTML and JavaScript.

---

## MQTT Data Generator in Python

The core simulation runs from a Python MQTT script featuring five main functions:

- **Temperature Generator**
- **Sunlight (Lux) Generator**
- **Radian (Sun Position) Generator**
- **MQTT Publisher**
- **Main Simulation Loop**:  
  - Executes for 1440 seconds (simulating 24 hours in 24 minutes).  
  - Publishes data every 20 seconds.

**Simulation Targets**:
- **ThingSpeak**: For channel-based field visualization.
- **Make.com**: For automation workflows.

> See `MQTT_Application.py` for the full implementation.

**Figure 0**: *MQTT IoT simulator using ThingSpeak*

---

## ThingSpeak Channel Setup

- **Temperature & Light Channels**:
  - 5 fields: `Device ID`, `North`, `East`, `South`, `West` window positions.
- **Radian Channel**:
  - 2 fields: `Radians` and `Device ID`.

### Observations:
- Light data varied by window direction (East = AM, West = PM).
- Radian data tracked sun’s arc from 0π to 2π.
- Temperature showed consistent diurnal cycles.

**Figures 1–4**:  
- Field chart configurations and data visualization in ThingSpeak (24 data points each).

---

## Make.com + Google Sheets + Webhooks

Three **scenarios** in Make.com:
- **Light Scenario**
- **Temperature Scenario**
- **Radian Scenario**

**Functionality**:
- Google Sheets logging with timestamps.
- Conditional triggers for blinds based on lux, temp, and radian values.
- Recalculated blind positions pushed to `webhook.site` as raw JSON.

**Figures 5–7**: Make.com scenarios  
**Figures 8–11**: Google Sheets population  
**Figures 12–14**: Lux-triggered blind angle recalculation  
**Figures 15–17**: JSON payloads received by webhook.site

---

## HTML Visualization of Average Temperature

A secondary Python script (`Generate_avgTemps_JSON_file.py`) fetches recent temperature data via ThingSpeak’s API and writes a JSON file with averaged values.

**Frontend Stack**:
- **JavaScript**:
  - Fetches JSON
  - Creates a rolling chart
  - Color-codes temperature zones (under, within, over)
- **HTML + CSS**:
  - Imports and displays the temperature graph
  - Uses `Chart.js` for rendering

> ⚠Due to browser security, a local server is required to enable `fetch()`.

**Figure 18**: Live graph of 24-point rolling average temperatures

---

## Results

This project successfully demonstrates a multi-component IoT system:
- Simulates environmental data via MQTT.
- Visualizes real-time metrics in ThingSpeak.
- Automates blind control based on environmental changes using Make.com.
- Pushes results to Google Sheets and webhook endpoints.
- Provides browser-based data visualization using JavaScript and HTML.

---

## Future Improvements

- Consolidate Python scripts for efficiency.
- Remove unnecessary steps like webhook.site (used for testing).
- Expand smart behavior logic for more dynamic real-world simulations.
- Integrate with real hardware (e.g., servo motors controlling actual blinds).
