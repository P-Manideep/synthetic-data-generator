import numpy as np


def create_ecommerce_scenario():
    
    def calculate_discount(order_value):
        if order_value > 500:
            return order_value * 0.15
        elif order_value > 200:
            return order_value * 0.10
        elif order_value > 100:
            return order_value * 0.05
        return 0
    
    def validate_total(df):
        expected_total = df['order_value'] - df['discount'] + df['shipping_cost']
        return np.allclose(df['total'], expected_total, rtol=0.01)
    
    scenario = {
        'columns': {
            'order_id': {
                'type': 'text',
                'template': 'ORD-{id:06d}'
            },
            'customer_segment': {
                'type': 'categorical',
                'categories': ['Premium', 'Standard', 'Basic'],
                'weights': [0.2, 0.5, 0.3]
            },
            'order_value': {
                'type': 'numeric',
                'distribution': 'normal',
                'mean': 150,
                'std': 75,
                'min': 10,
                'max': 1000
            },
            'order_date': {
                'type': 'datetime',
                'start': '2024-01-01',
                'end': '2024-12-31'
            },
            'shipping_cost': {
                'type': 'numeric',
                'distribution': 'uniform',
                'min': 5,
                'max': 25
            },
            'discount': {
                'type': 'numeric',
                'distribution': 'uniform',
                'min': 0,
                'max': 1
            },
            'total': {
                'type': 'numeric',
                'distribution': 'uniform',
                'min': 0,
                'max': 1
            }
        },
        'dependencies': [
            {
                'target': 'discount',
                'source': 'order_value',
                'rule': calculate_discount
            }
        ],
        'validations': []
    }
    
    return scenario


def create_fraud_detection_scenario():
    
    scenario = {
        'columns': {
            'transaction_id': {
                'type': 'text',
                'template': 'TXN-{id:08d}'
            },
            'amount': {
                'type': 'numeric',
                'distribution': 'exponential',
                'scale': 100,
                'min': 1,
                'max': 5000
            },
            'transaction_type': {
                'type': 'categorical',
                'categories': ['purchase', 'withdrawal', 'transfer', 'payment'],
                'weights': [0.5, 0.2, 0.2, 0.1]
            },
            'is_international': {
                'type': 'categorical',
                'categories': [True, False],
                'weights': [0.15, 0.85]
            },
            'time_since_last_transaction': {
                'type': 'numeric',
                'distribution': 'exponential',
                'scale': 3600,
                'min': 60,
                'max': 86400
            },
            'device_type': {
                'type': 'categorical',
                'categories': ['mobile', 'desktop', 'tablet'],
                'weights': [0.6, 0.3, 0.1]
            },
            'is_fraud': {
                'type': 'categorical',
                'categories': [True, False],
                'weights': [0.02, 0.98]
            }
        },
        'dependencies': [],
        'validations': []
    }
    
    return scenario


def create_sensor_data_scenario():
    
    scenario = {
        'columns': {
            'sensor_id': {
                'type': 'categorical',
                'categories': [f'SENSOR-{i:03d}' for i in range(1, 51)]
            },
            'timestamp': {
                'type': 'datetime',
                'start': '2024-01-01 00:00:00',
                'end': '2024-01-31 23:59:59'
            },
            'temperature': {
                'type': 'numeric',
                'distribution': 'normal',
                'mean': 22.5,
                'std': 3.0,
                'min': 15,
                'max': 30
            },
            'humidity': {
                'type': 'numeric',
                'distribution': 'normal',
                'mean': 45,
                'std': 10,
                'min': 20,
                'max': 80
            },
            'pressure': {
                'type': 'numeric',
                'distribution': 'normal',
                'mean': 1013,
                'std': 5,
                'min': 1000,
                'max': 1030
            },
            'status': {
                'type': 'categorical',
                'categories': ['normal', 'warning', 'critical'],
                'weights': [0.85, 0.12, 0.03]
            }
        },
        'dependencies': [],
        'validations': []
    }
    
    return scenario


def create_customer_churn_scenario():
    
    def calculate_churn(tenure_months):
        if tenure_months < 6:
            return np.random.choice([True, False], p=[0.3, 0.7])
        elif tenure_months < 12:
            return np.random.choice([True, False], p=[0.15, 0.85])
        else:
            return np.random.choice([True, False], p=[0.05, 0.95])
    
    scenario = {
        'columns': {
            'customer_id': {
                'type': 'text',
                'template': 'CUST-{id:06d}'
            },
            'tenure_months': {
                'type': 'numeric',
                'distribution': 'exponential',
                'scale': 12,
                'min': 1,
                'max': 72
            },
            'monthly_charges': {
                'type': 'numeric',
                'distribution': 'normal',
                'mean': 65,
                'std': 30,
                'min': 20,
                'max': 150
            },
            'total_charges': {
                'type': 'numeric',
                'distribution': 'uniform',
                'min': 0,
                'max': 1
            },
            'contract_type': {
                'type': 'categorical',
                'categories': ['Month-to-month', 'One year', 'Two year'],
                'weights': [0.5, 0.3, 0.2]
            },
            'payment_method': {
                'type': 'categorical',
                'categories': ['Electronic check', 'Credit card', 'Bank transfer', 'Mailed check'],
                'weights': [0.4, 0.3, 0.2, 0.1]
            },
            'has_churned': {
                'type': 'categorical',
                'categories': [True, False],
                'weights': [0.2, 0.8]
            }
        },
        'dependencies': [
            {
                'target': 'has_churned',
                'source': 'tenure_months',
                'rule': calculate_churn
            }
        ],
        'validations': []
    }
    
    return scenario