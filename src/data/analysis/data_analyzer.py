from pathlib import Path
from typing import Optional

import pandas as pd

from src.data.analysis.hist_feature_generator import HistFeatureGenerator


class DataAnalyzer:
    def __init__(self,
                 dataset: Optional[pd.DataFrame] = None,
                 n_races: int = 5,
                 n_days: int = 180
                 ):
        self.dataset = dataset

        self.historical_features = list()

        if dataset is not None:
            new_cols = self.get_historical_features(
                n_races=n_races, n_days=n_days
            )

            self.dataset = pd.concat(
                objs=[
                    self.dataset,
                    pd.DataFrame(new_cols)
                ], axis=1
            ).copy()
            self.dataset = self.dataset.loc[:, ~self.dataset.columns.duplicated()].copy()

            self.historical_features = list(new_cols.keys())

    def save_dataset(self, path: Path):
        self.dataset.to_pickle(path)

    def load_dataset(self, path: Path):
        self.dataset = pd.read_pickle(path)
        self.historical_features = [
            'horse_race_count', 'horse_avg_fp_target_surf', 'horse_avg_fp_other_surf',
            'horse_avg_fp', 'horse_avg_l3f', 'horse_win_rate', 'horse_fp_momentum',
            'horse_weight_dev_avg', 'days_since_last', 'jockey_win_rate',
            'trainer_win_rate', 'owner_win_rate'
        ]

    def get_historical_features(self,
                                n_races: int,
                                n_days: int
                                ):
        calculation_cols = [
            'race_date', 'horse_name', 'horse_weight', 'turf_or_dirt',
            'fp', 'l3f', 'jockey', 'trainer', 'owner'
        ]
        return HistFeatureGenerator.generate_historical_features(
            dataset=self.dataset[calculation_cols],
            n_races=n_races, n_days=n_days
        )
