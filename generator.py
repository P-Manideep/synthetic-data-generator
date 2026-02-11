import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any


class ScenarioDataGenerator:
    
    def __init__(self, scenario_config: Dict[str, Any]):
        self.config = scenario_config
        self.validators = []
        
    def generate_dataset(self, num_records: int) -> pd.DataFrame:
        print(f"\n🔄 Generating {num_records} records...")
        data = {}
        
        for column, rules in self.config['columns'].items():
            print(f"  ✓ Generating column: {column}")
            data[column] = self._generate_column(column, rules, num_records)
        
        df = pd.DataFrame(data)
        
        print("\n🔗 Applying dependencies...")
        df = self._apply_dependencies(df)
        
        print("🔒 Applying constraints...")
        df = self._apply_constraints(df)
        
        print("\n✅ Validating data...")
        self._validate_data(df)
        
        return df
    
    def _generate_column(self, column_name: str, rules: Dict, num_records: int) -> List:
        col_type = rules.get('type')
        
        if col_type == 'categorical':
            return self._generate_categorical(rules, num_records)
        elif col_type == 'numeric':
            return self._generate_numeric(rules, num_records)
        elif col_type == 'datetime':
            return self._generate_datetime(rules, num_records)
        elif col_type == 'text':
            return self._generate_text(rules, num_records)
        else:
            raise ValueError(f"Unknown column type: {col_type}")
    
    def _generate_categorical(self, rules: Dict, num_records: int) -> List:
        categories = rules['categories']
        weights = rules.get('weights')
        
        if weights:
            return np.random.choice(categories, size=num_records, p=weights)
        return np.random.choice(categories, size=num_records)
    
    def _generate_numeric(self, rules: Dict, num_records: int) -> np.ndarray:
        distribution = rules.get('distribution', 'uniform')
        min_val = rules.get('min', 0)
        max_val = rules.get('max', 100)
        
        if distribution == 'uniform':
            return np.random.uniform(min_val, max_val, num_records)
        elif distribution == 'normal':
            mean = rules.get('mean', (min_val + max_val) / 2)
            std = rules.get('std', (max_val - min_val) / 6)
            return np.clip(np.random.normal(mean, std, num_records), min_val, max_val)
        elif distribution == 'exponential':
            scale = rules.get('scale', 1.0)
            return np.random.exponential(scale, num_records)
        
    def _generate_datetime(self, rules: Dict, num_records: int) -> List:
        start_date = pd.to_datetime(rules['start'])
        end_date = pd.to_datetime(rules['end'])
        
        time_delta = (end_date - start_date).total_seconds()
        random_seconds = np.random.randint(0, time_delta, num_records)
        
        return [start_date + timedelta(seconds=int(s)) for s in random_seconds]
    
    def _generate_text(self, rules: Dict, num_records: int) -> List:
        template = rules.get('template')
        patterns = rules.get('patterns', [])
        
        if template:
            return [template.format(id=i) for i in range(num_records)]
        elif patterns:
            return np.random.choice(patterns, size=num_records)
        
    def _apply_dependencies(self, df: pd.DataFrame) -> pd.DataFrame:
        dependencies = self.config.get('dependencies', [])
        
        for dep in dependencies:
            target_col = dep['target']
            source_col = dep['source']
            rule_func = dep['rule']
            
            df[target_col] = df[source_col].apply(rule_func)
        
        return df
    
    def _apply_constraints(self, df: pd.DataFrame) -> pd.DataFrame:
        constraints = self.config.get('constraints', [])
        
        for constraint in constraints:
            constraint_func = constraint['function']
            df = df[constraint_func(df)]
        
        return df.reset_index(drop=True)
    
    def _validate_data(self, df: pd.DataFrame):
        validations = self.config.get('validations', [])
        
        for validation in validations:
            validation_func = validation['function']
            error_msg = validation.get('error_message', 'Validation failed')
            
            if not validation_func(df):
                raise ValueError(error_msg)
        
        print(f"✓ Generated {len(df)} records")
        print(f"✓ All {len(validations)} validations passed")