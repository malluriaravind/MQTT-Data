# MQTT Data Publishing and Subscription System

## Overview
This document provides an overview of the implemented MQTT data publishing and subscription system. The system is designed to collect Water Mark Levels (WML) from various reservoirs and aggregate this data for reporting purposes.

## Components
1. **Publisher**: This component reads data from CSV files containing WML for different reservoirs (Shasta, Oroville, Sonoma) and publishes the data to specific MQTT topics in JSON format.
2. **Subscriber**: This component subscribes to the relevant MQTT topics and collects the published data. It generates daily reports based on the collected data and saves them in CSV format.

## Data Flow
- **Data Sources**: The system uses CSV files as the data source for reservoir water levels. Each reservoir has its respective CSV file.
- **MQTT Protocol**: The data is published to the MQTT broker (RabbitMQ with the MQTT plugin) using specific topics formatted as `Reservoir_ID/WML` (e.g., `SHASTA/WML`).
- **JSON Format**: The messages published to the MQTT broker are structured in JSON format, containing fields such as `Reservoir_ID`, `Timestamp`, and `WaterLevel_TAF`.

## Reporting
- The subscriber component aggregates the collected data to produce daily summaries, including:
  - Minimum Water Level
  - Maximum Water Level
  - Average Water Level
- The aggregated reports are displayed in the console and saved as a CSV file (`daily_report.csv`). The reports can also be converted to JSON format for further use.

## Libraries Used
- **Paho MQTT**: A client library for MQTT used for connecting, publishing, and subscribing to topics.
- **Pandas**: A data manipulation library used for handling CSV data and generating reports.

## Usage Instructions
1. Ensure RabbitMQ is installed and running with the MQTT plugin enabled.
2. Place the CSV files for the reservoirs in the same directory as the scripts.
3. Run the publisher script to start publishing data to the MQTT topics.
4. Run the subscriber script to start collecting data and generating reports.

## Conclusion
This system provides an efficient way to monitor and report on water levels across multiple reservoirs using MQTT. The modular design allows for easy updates and integration with other data sources or reporting formats in the future.
