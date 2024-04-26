import pandas as pd
import json

class DatasetCreator:
    def __init__(self, json_path, csv_path):
        self.json_path = json_path
        self.csv_path = csv_path

    def create_dataset(self):
        # Load data from JSON file
        with open(self.json_path, 'r') as f:
            data = json.load(f)

        # Create DataFrame
        df = pd.DataFrame(data)

        # Write DataFrame to CSV
        df.to_csv(self.csv_path, index=False)

        return df