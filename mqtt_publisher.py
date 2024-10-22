import paho.mqtt.client as mqtt
import json
import pandas as pd

# Define the MQTT broker address and port
BROKER_ADDRESS = "localhost"  # Use "localhost" if RabbitMQ is running locally
BROKER_PORT = 1883

def load_data():
    """Load data from CSV files and return as a dictionary."""
    data_files = {
        "SHASTA": 'Shasta_WML(Sample).csv',
        "OROVILLE": 'Oroville_WML(Sample).csv',
        "SONOMA": 'Sonoma_WML(Sample).csv'
    }
    return {key: pd.read_csv(file) for key, file in data_files.items()}

def publish_data(client, reservoir_id, data):
    """Publish data to a specific MQTT topic."""
    for _, row in data.iterrows():
        message = {
            "Reservoir_ID": reservoir_id,
            "Timestamp": row['Date'],
            "WaterLevel_TAF": row['TAF']
        }
        topic = f"{reservoir_id}/WML"
        result = client.publish(topic, json.dumps(message))
        if result.rc == mqtt.MQTT_ERR_NO_CONN:
            print("Error: Not connected to MQTT broker.")
        else:
            print(f"Published to {topic}: {message}")

def main():
    # Load data
    reservoir_data = load_data()

    # Initialize MQTT client
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

    # Publish data for each reservoir
    for reservoir_id, data in reservoir_data.items():
        publish_data(client, reservoir_id, data)

    client.disconnect()

if __name__ == "__main__":
    main()
