import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from src.data.data_transformer import DataTransformer
from src.data.data_translator import DataTranslator


class DataAnalyzer:
    def __init__(self,
                 data_translator: DataTranslator
                 ):
        self.dataset = DataTransformer.merge_data(data_translator=data_translator)
        self.dataset['race_date'] = pd.to_datetime(self.dataset['race_date'])
        self.dataset = self.dataset.sort_values(by=['race_date', 'race_id', 'pp'], kind='mergesort')
        self.dataset.dropna(subset=['fp'], inplace=True)
        self.dataset['track_direction'] = self.dataset['track_direction'].fillna('Straight')

        self.numerical_features = [
            'distance',
            'pp',
            'age',
            'weight',
            'horse_weight',
            'horse_weight_diff'
        ]
        self.categorical_features = [
            'racecourse_name',
            'race_cond',
            'turf_or_dirt',
            'track_direction',
            'weather',
            'sex',
            'stable_region'
        ]
        self.ordinal_features = [
            'track_cond'
        ]

        self.feature_cols = (
            self.numerical_features +
            self.categorical_features +
            self.ordinal_features
        )

        management_cols = ['race_id', 'race_date', 'horse_name', 'fp']
        calculation_cols = ['l3f', 'jockey', 'trainer', 'owner']

        all_cols = self.feature_cols + management_cols + calculation_cols
        self.dataset = self.dataset[all_cols]

        self.new_cols = dict()
        self.generate_historical_features(n_races=5, n_days=365)

        self.dataset = self.dataset.drop(
            columns=calculation_cols
        )

        self.pipeline = self.get_preprocessing_pipeline()

    def generate_historical_features(self, n_races: int, n_days: int):
        is_winner_series = pd.Series((self.dataset['fp'] == 1) * 1)

        self.new_cols['horse_win_rate'] = (
            is_winner_series.groupby(
                by=self.dataset['horse_name'],
                observed=True, sort=False
            )
            .rolling(window=n_races).mean()
            .reset_index(level=0, drop=True)
            .shift(1).values
        )

        horse_grouping = self.dataset.groupby(
            by='horse_name',
            observed=True, sort=False
        )

        self.new_cols['horse_race_count'] = (
            horse_grouping.cumcount()
        )

        for surface in ['Turf', 'Dirt']:
            mask = (self.dataset['turf_or_dirt'] == surface)
            surface_fp = self.dataset['fp'].where(mask)
            col_name = f'horse_avg_fp_{surface.lower()}'
            self.new_cols[col_name] = (
                surface_fp.groupby(by=self.dataset['horse_name'], observed=True, sort=False)
                .rolling(window=n_races, min_periods=1).mean()
                .reset_index(level=0, drop=True).shift(1).values
            )

        def get_avg_horse_data(target_col: str
                               ) -> np.ndarray:
            return (
                horse_grouping[target_col]
                .rolling(window=n_races).mean()
                .reset_index(level=0, drop=True)
                .shift(1).values
            )

        self.new_cols['horse_avg_fp'] = get_avg_horse_data(target_col='fp')
        self.new_cols['horse_avg_l3f'] = get_avg_horse_data(target_col='l3f')
        self.new_cols['days_since_last'] = (
            horse_grouping['race_date']
            .diff().dt.days
        )

        for col in ['jockey', 'trainer', 'owner']:
            temp = self.dataset[[col, 'race_date']].copy()
            temp['is_winner'] = is_winner_series.values

            self.new_cols[f'{col}_win_rate'] = (
                temp.groupby(
                    by=col,
                    observed=True, sort=False
                )
                .rolling(
                    on='race_date', window=f'{n_days}D', closed='left'
                )['is_winner'].mean()
                .reset_index(level=0, drop=True)
                .values
            )

        self.dataset = pd.concat(
            objs=[
                self.dataset,
                pd.DataFrame(self.new_cols)
            ], axis=1
        ).copy()
        self.dataset = self.dataset.loc[:, ~self.dataset.columns.duplicated()].copy()

    def get_preprocessing_pipeline(self):
        column_transformer = ColumnTransformer(
            transformers=[
                ('num', Pipeline([
                    ('impute', SimpleImputer(strategy='median')),
                    ('scale', StandardScaler())
                ]), self.numerical_features),

                ('hist', Pipeline([
                    ('impute', SimpleImputer(strategy='constant', fill_value=-1)),
                    ('scale', StandardScaler())
                ]), list(self.new_cols.keys())),

                ('cat', Pipeline([
                    ('impute', SimpleImputer(strategy='most_frequent')),
                    ('ord', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
                ]), self.categorical_features),

                ('ord', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1),
                 self.ordinal_features)
            ],
            remainder='drop'
        )
        column_transformer.set_output(transform='pandas')
        return column_transformer
