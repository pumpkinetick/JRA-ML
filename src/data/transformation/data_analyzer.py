import pandas as pd

from src.data.transformation.hist_feature_generator import HistFeatureGenerator


class DataAnalyzer:
    def __init__(self,
                 dataset: pd.DataFrame,
                 n_races: int = 5,
                 n_days: int = 180
                 ):
        self.dataset = dataset

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
