from src.data.data_loader import DataLoader
from src.data.utilities import load_from_json


class DataTranslator:
    def __init__(self,
                 data_loader: DataLoader
                 ):
        self.data_path = data_loader.data_path

        self.corner_passing_orders = data_loader.corner_passing_orders
        self.translate_corner_passing_orders()

        self.laptimes = data_loader.laptimes
        self.translate_laptimes()

        self.odds = data_loader.odds
        self.translate_odds()

        self.race_results = data_loader.race_results
        self.translate_race_results()

    def translate_corner_passing_orders(self):
        col_map = load_from_json(
            self.data_path / 'corner_passing_orders_col_map.json'
        )
        self.corner_passing_orders.rename(columns=col_map, inplace=True)

    def translate_laptimes(self):
        col_map = load_from_json(
            self.data_path / 'laptimes_col_map.json'
        )
        self.laptimes.rename(columns=col_map, inplace=True)

    def translate_odds(self):
        column_map = load_from_json(
            self.data_path / 'odds_col_map.json'
        )
        self.odds.rename(columns=column_map, inplace=True)

    def translate_race_results(self):
        col_map = load_from_json(
            self.data_path / 'race_results_col_map.json'
        )
        self.race_results.rename(columns=col_map, inplace=True)

        symbol_cols = [col for col in self.race_results.columns if col.startswith('symbol_')]
        for col in symbol_cols:
            self.race_results[col] = self.race_results[col].notna().astype(int)

        entry_map = load_from_json(
            self.data_path / 'race_results_entry_map.json'
        )
        for col, mapping in entry_map.items():
            if col in self.race_results.columns:
                self.race_results[col] = self.race_results[col].replace(mapping)

        margin_sub_map = load_from_json(
            self.data_path / 'margin_sub_map.json'
        )
        for jp, en in margin_sub_map.items():
            self.race_results['margin'] = self.race_results['margin'].str.replace(jp, en, regex=False)

        self.race_results['race_cond'] = self.race_results['race_cond'].str.strip()

        self.race_results['steeplechase_cat'] = self.race_results['steeplechase_cat'].fillna('Flat')
        self.race_results.loc[self.race_results['steeplechase_cat'] == '障害', 'steeplechase_cat'] = 'Steeplechase'

        race_cond_map = load_from_json(
            self.data_path / 'race_cond_map.json'
        )
        self.race_results['race_cond'] = self.race_results['race_cond'].replace(race_cond_map)
