# Synthetic Data Generator

A Python project that generates realistic synthetic data for testing ML models, dashboards, and data pipelines.

## Features

- 🎯 4 Pre-built Scenarios: E-commerce, Fraud Detection, IoT Sensors, Customer Churn
- 📊 Realistic Data: Uses statistical distributions and business rules
- ⚡ Easy to Use: Interactive CLI interface
- 📁 CSV Output: Ready for immediate use

## Installation
```bash
pip install pandas numpy
```

## Usage
```bash
python main.py
```

Then select a scenario and enter the number of records to generate.

## Scenarios

### 1. E-commerce Orders
Generates order data with customer segments, discounts, and shipping costs.

### 2. Fraud Detection
Transaction data with fraud indicators for testing detection systems.

### 3. IoT Sensor Data
Temperature, humidity, and pressure readings from multiple sensors.

### 4. Customer Churn
Customer subscription data with churn predictions based on tenure.

## Output

The program generates a CSV file with realistic data based on your selected scenario.

## Requirements

- Python 3.8+
- pandas 2.0.3
- numpy 1.24.3

## License

MIT License