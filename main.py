from generator import ScenarioDataGenerator
from scenarios import (
    create_ecommerce_scenario,
    create_fraud_detection_scenario,
    create_sensor_data_scenario,
    create_customer_churn_scenario
)
import pandas as pd


def main():
    print("=" * 60)
    print("SYNTHETIC DATA GENERATOR")
    print("=" * 60)
    
    print("\nAvailable Scenarios:")
    print("1. E-commerce Orders")
    print("2. Fraud Detection")
    print("3. IoT Sensor Data")
    print("4. Customer Churn")
    
    choice = input("\nSelect scenario (1-4): ").strip()
    
    scenarios = {
        '1': ('ecommerce', create_ecommerce_scenario),
        '2': ('fraud_detection', create_fraud_detection_scenario),
        '3': ('sensor_data', create_sensor_data_scenario),
        '4': ('customer_churn', create_customer_churn_scenario)
    }
    
    if choice not in scenarios:
        print("❌ Invalid choice!")
        return
    
    scenario_name, scenario_func = scenarios[choice]
    
    num_input = input("Enter number of records to generate (default 1000): ").strip()
    num_records = int(num_input) if num_input else 1000
    
    print(f"\n📋 Loading {scenario_name} scenario...")
    scenario = scenario_func()
    
    generator = ScenarioDataGenerator(scenario)
    df = generator.generate_dataset(num_records=num_records)
    
    if scenario_name == 'ecommerce':
        df['total'] = df['order_value'] - df['discount'] + df['shipping_cost']
    elif scenario_name == 'customer_churn':
        df['total_charges'] = df['tenure_months'] * df['monthly_charges']
    
    print("\n" + "=" * 60)
    print("GENERATED DATA SAMPLE (First 10 rows)")
    print("=" * 60)
    print(df.head(10).to_string())
    
    print("\n" + "=" * 60)
    print("DATA STATISTICS")
    print("=" * 60)
    print(df.describe())
    
    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)
    print(df.dtypes)
    
    output_file = f"{scenario_name}_synthetic_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Data saved to: {output_file}")
    
    print("\n" + "=" * 60)
    print("DATA INSIGHTS")
    print("=" * 60)
    
    if scenario_name == 'ecommerce':
        print(f"Total Orders: {len(df)}")
        print(f"Total Revenue: ${df['order_value'].sum():,.2f}")
        print(f"Average Order Value: ${df['order_value'].mean():.2f}")
        print(f"Total Discounts: ${df['discount'].sum():,.2f}")
        print(f"\nCustomer Segment Distribution:")
        print(df['customer_segment'].value_counts())
        
    elif scenario_name == 'fraud_detection':
        print(f"Total Transactions: {len(df)}")
        print(f"Fraud Cases: {df['is_fraud'].sum()}")
        print(f"Fraud Rate: {df['is_fraud'].mean() * 100:.2f}%")
        print(f"Total Transaction Amount: ${df['amount'].sum():,.2f}")
        print(f"\nTransaction Type Distribution:")
        print(df['transaction_type'].value_counts())
        
    elif scenario_name == 'sensor_data':
        print(f"Total Readings: {len(df)}")
        print(f"Unique Sensors: {df['sensor_id'].nunique()}")
        print(f"Avg Temperature: {df['temperature'].mean():.2f}°C")
        print(f"Avg Humidity: {df['humidity'].mean():.2f}%")
        print(f"\nStatus Distribution:")
        print(df['status'].value_counts())
        
    elif scenario_name == 'customer_churn':
        print(f"Total Customers: {len(df)}")
        print(f"Churned Customers: {df['has_churned'].sum()}")
        print(f"Churn Rate: {df['has_churned'].mean() * 100:.2f}%")
        print(f"Avg Monthly Charges: ${df['monthly_charges'].mean():.2f}")
        print(f"\nContract Type Distribution:")
        print(df['contract_type'].value_counts())
    
    print("\n" + "=" * 60)
    print("✅ GENERATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()