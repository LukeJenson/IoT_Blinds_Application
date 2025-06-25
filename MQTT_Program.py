import paho.mqtt.client as mqtt
import time
import math
import requests
import random
# MQTT information
broker = "mqtt3.thingspeak.com"
port = 1883
username = "MwEJFyE5DCMGAx0CLjEqMSs"
client_id = "MwEJFyE5DCMGAx0CLjEqMSs"
password = "FDSbSegzzzmQSts8mWEuQTz3"
# Webhook pathway
temp_webhook_url = "https://hook.us2.make.com/z3ytjvmljmadsl8qsvxuor2u1gerxm9n"
light_webhook_url = "https://hook.us2.make.com/jd18lrl0357mdqbs3vawyg4qu2cljuvq"
rad_webhook_url = "https://hook.us2.make.com/g78m5n1qftm29ntoxejgn8d3ng6wcpqs"
# Channel Paths and Device IDs
temp_topic = "channels/2984145/publish"
temp_dev = "28-7654321"
lux_topic = "channels/2984167/publish"
lux_dev ="28-6543211"
radian_topic = "channels/2984172/publish"
rad_dev = "28-5432111"
# Function Called to Publish Data to ThingSpeak and Make.com.
def publish(client, topic, payload,make_webhook_url, webhook_payload):
    client.publish(topic, payload)
    requests.post(make_webhook_url, json=webhook_payload)
# Function simulating window temperatures.
def temperature(client, t):
    # Defines parameters for sin() wave changes.
    base = 60
    amplitude = 50
    epsilon = 0.0134 * math.pi # Radial phase shift (represents ~0.1F).
    # Offset temperature phases (different windows experience different temperature).
    phase_W = -math.pi / 2
    phase_N = (-math.pi / 2) + (2 * epsilon)
    phase_S = (-math.pi / 2) + (2 * epsilon)
    phase_E = (-math.pi / 2) + (4 * epsilon)
    # Oscillations with phase shifts
    temp_W = base + amplitude * math.sin(2 * math.pi * t + phase_W)
    temp_N = base + amplitude * math.sin(2 * math.pi * t + phase_N)
    temp_S = base + amplitude * math.sin(2 * math.pi * t + phase_S)
    temp_E = base + amplitude * math.sin(2 * math.pi * t + phase_E)
    # Defines temp payloads for ThingSpeak.
    payload = f"field1={round(temp_N, 2)}&field2={round(temp_E, 2)}&field3={round(temp_S, 2)}&field4={round(temp_W, 2)}&field5={temp_dev}"
    # Defines temp payloads for Make.com. 
    web_payload = {
        "Device_ID": temp_dev,
        "Temp_N": round(temp_N, 2),
        "Temp_E": round(temp_E, 2),
        "Temp_S": round(temp_S, 2),
        "Temp_W": round(temp_W, 2)
    }
    # Calls publish function passing in payloads and global variables.
    publish(client, temp_topic, payload,temp_webhook_url, web_payload)
    # Displays temperature values published.
    print(f'Temperatures Published (N,E,S,W): {round(temp_N, 2)}, {round(temp_E, 2)}, {round(temp_S, 2)}, {round(temp_W, 2)}')
# Function simulating different light measurements.
def sunlight(client, step):
    lux_N = lux_E = lux_S = lux_W = 0.0 # Establishes Lux value of no light.
    t = int((step-1)/3) # Normalizes the step value (t represents single hour).
    if t < 13: # performs for daylight intervals
        lux_N = lux_S = ((-(5/18) * (t**2)) + ((10/3)*t)) * 7500 # Quadratic representation of sunlight even distribution throughout day.
        if t<=3:
            lux_E = ((-(10/9) * (t**2)) + ((20/3)*t)) * 10000 # Sun rises in the East / Light hits E sensor first.
        elif t > 3 and t <= 12:
            lux_E = ((-(10/81) * (t**2)) + ((20/27)*t) + (80/9)) * 10000 # Sunlight dissipates back to lux = 0 gradually.
        if t < 9:
            lux_W = ((-(10/81) * (t**2)) + ((20/9)*t)) * 10000 # Sunlight gradually grows from 0 until 9th hour.
        elif t >= 9 and t <= 12:
            lux_W = ((-(10/9) * (t**2)) + (20*t) - (80)) * 10000 # Sun sets in West / Light hits W sensor last.
    if lux_N <= 0.0: # Night Hours: simulates street-lights, moonlight, and light-pollution.
        lux_N = random.randint(100, 1000)
        lux_E = random.randint(100, 1000)
        lux_S = random.randint(100, 1000)
        lux_W = random.randint(100, 1000)   
    # Defines lux payloads for ThingSpeak
    payload = f"field1={int(round(lux_N))}&field2={int(round(lux_E))}&field3={int(round(lux_S))}&field4={int(round(lux_W))}&field5={lux_dev}"
    # Defines Lux payloads for Make.com. 
    web_payload = {
        "Device_ID": f"{lux_dev}",
        "Lux_N": int(round(lux_N, 0)),
        "Lux_E": int(round(lux_E, 0)),
        "Lux_S": int(round(lux_S, 0)),
        "Lux_W": int(round(lux_W, 0))}
    # Calls publish function passing payloads and global variables.
    publish(client, lux_topic, payload, light_webhook_url, web_payload)
    # Displays lux values published.
    print(f"Publishing Lux (N, E, S, W): {lux_N: 0}, {lux_E: 0}, {lux_S: 0}, {lux_W: 0}")
# Defines function to simulate sun (radial) position.
def radian(client, t):
    # Simulates sun position
    radian = 2 * math.pi * t  # 0 to ~2pi radians
    # Defines sun (radial) payload for ThingSpeak.
    payload = f"field1={radian:.4f}&field2={rad_dev}"
    # Defines sun (radial) payload for Make.com.
    web_payload = {
        "Device_ID": f"{rad_dev}",
        "Radian": round(radian, 3)}
    # Calls publish function passing in payloads and global variables.
    publish(client, radian_topic, payload, rad_webhook_url, web_payload)
    # Displays radial values published.
    print(f'Published radial value: {round(radian, 3)}')
# Main function for calling simulation.
def main():
    # Establishes MQTT client connection.   
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker, port, 60)
    # Variables for looping
    total_duration_sec = 1440 # Represents total length of 24hrs in 1440 seconds.
    interval_sec = 20 # Represents measurements taken at 20min intervals in 20 seconds (ThingSpeak 15sec min).
    steps = total_duration_sec // interval_sec # Total calls in daily execution.
    # Loops for daily cycle.
    for step in range(steps):
        cycle_pos = step % 3 # Remainder divisible by 3.
        t = step / steps
        if cycle_pos == 0: # Publishes Temp on first 20 second interval (0, 60, 120...)
            temperature(client, t)    
        elif cycle_pos == 1: # Publishes Lux on second 20 second interval (20, 80, 140...)
            sunlight(client, step)
        else: # Publishes Radians on third 20 second interval (40, 100, 160...).
            radian(client, t)
        # Runs Loop on established time interval (min 15seconds ThingSpeak requirement).
        time.sleep(interval_sec)        
    client.disconnect() # Disconnects from MQTT device.
    
if __name__ == "__main__":
    main()