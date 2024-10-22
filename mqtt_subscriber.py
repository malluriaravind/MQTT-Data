import paho.mqtt.client as mqtt
import json
import pandas as pd
import time

reservoir_data = []

# Define the MQTT broker address and port
BROKER_ADDRESS = "localhost"  # Use "localhost" if RabbitMQ is running locally
BROKER_PORT = 1883

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("+/WML")  # Subscribe to all reservoir topics
        print("Subscribed to topics: +/WML")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback for when a message is received."""
    data = json.loads(msg.payload)
    print(f"Received data: {data}")
    reservoir_data.append(data)

def generate_report():
    """Generate and save a daily report from the collected data."""
    if reservoir_data:
        df = pd.DataFrame(reservoir_data)

        required_columns = {'Reservoir_ID', 'Timestamp', 'WaterLevel_TAF'}
        if not required_columns.issubset(df.columns):
            print(f"Missing required columns. Available columns are: {df.columns.tolist()}")
            return

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Date'] = df['Timestamp'].dt.date

        report = df.groupby(['Reservoir_ID', 'Date']).agg(
            Min_WaterLevel_TAF=('WaterLevel_TAF', 'min'),
            Max_WaterLevel_TAF=('WaterLevel_TAF', 'max'),
            Average_WaterLevel_TAF=('WaterLevel_TAF', 'mean')
        ).reset_index()

        print("Daily Report:")
        print(report)

        report.to_csv('daily_report.csv', index=False)
        print("Report saved to daily_report.csv.")

        report_json = report.to_json(orient="records", date_format="iso")
        print("Generated Daily Report in JSON format:", report_json)
    else:
        print("No data collected during the subscription.")

def main():
    """Main function to set up the MQTT client and start listening."""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    client.loop_start()  # Start the loop to listen for messages

    time.sleep(60)  # Run for 60 seconds to allow time to collect messages

    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect from the broker

    generate_report()  # Generate and save the report

if __name__ == "__main__":
    main()
