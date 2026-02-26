from pathlib import Path

import pandas as pd


class DataLoader:
    def __init__(self,
                 data_path: Path
                 ):
        self.data_path = data_path

        self.corner_passing_orders = pd.DataFrame()
        self.laptimes = pd.DataFrame()
        self.odds = pd.DataFrame()
        self.race_results = pd.DataFrame()

        self.load_data()

    def load_data(self):
        for file_name in ['corner_passing_orders', 'laptimes', 'odds', 'race_results']:
            setattr(
                self, file_name,
                pd.read_csv(
                    self.data_path / f'{file_name}.csv'
                )
            )
