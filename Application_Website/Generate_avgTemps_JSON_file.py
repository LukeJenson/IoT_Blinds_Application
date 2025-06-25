import requests
import time
import json
from datetime import datetime
# ThingSpeak Read Channel settings
channel_id = 2984145 # Reads Temperature Channel.
api_url = f'https://api.thingspeak.com/channels/{channel_id}/fields/{{}}/last.json'
# Fields: N, E, S, W
fields = {"N": 1, "E": 2, "S": 3, "W": 4}
# Output temperature file path.
output_file = 'avgTemps.json'
# temp and time list storages.
avg_temps = []
timestamps = []
# Loop for 24 readings (one every 60 seconds)
for i in range(24):
    try:
        temps = [] # Temporary temperature list for ThingSpeak values.
        # Loops over all fields.
        for direction, field_id in fields.items():
            res = requests.get(api_url.format(field_id))
            data = res.json()
            temp = float(data['field' + str(field_id)])
            temps.append(temp) # Appends N, E, S, W ThingSpeak temps.
        avg_temp = sum(temps) / len(temps) # Calculates Building Temp (Average Temp).
        avg_temps.append(avg_temp) # Appends average temperature to avg_temps list.
        timestamps.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) # Appends time stamp.
        # Saves to JSON temperature file.
        out = [{"time": t, "avgTemp": a} for t, a in zip(timestamps, avg_temps)]
        with open(output_file, 'w') as f:
            json.dump(out, f, indent=2)
        # Displays average temperature
        print(f"[{i+1}/24] Avg Temp: {avg_temp:.2f} °F")
    except Exception as e:
        print(f"Error at step {i+1}: {e}")
    # Executes on 60 second intervals.
    if i < 23:
        time.sleep(60)  # Wait 60s before next reading

print("✅ Done logging 24 temperature readings.")
