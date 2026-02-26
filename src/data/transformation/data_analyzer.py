import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from src.data.preparation.data_translator import DataTranslator
from src.data.transformation.data_transformer import DataTransformer
from src.data.transformation.hist_feature_generator import HistFeatureGenerator


class DataAnalyzer:
    def __init__(self,
                 data_translator: DataTranslator,
                 numerical_features: list,
                 categorical_features: list,
                 ordinal_features: list,
                 n_races: int = 5,
                 n_days: int = 180
                 ):
        self.dataset = DataTransformer.merge_data(data_translator=data_translator)
        self.dataset['race_date'] = pd.to_datetime(self.dataset['race_date'])
        self.dataset = self.dataset.sort_values(by=['race_date', 'race_id', 'pp'], kind='mergesort')
        self.dataset.dropna(subset=['fp'], inplace=True)
        self.dataset['track_direction'] = self.dataset['track_direction'].fillna('Straight')
        self.dataset.reset_index(drop=True, inplace=True)

        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
        self.ordinal_features = ordinal_features

        calculation_cols = [
            'race_date', 'horse_name', 'horse_weight', 'turf_or_dirt',
            'fp', 'l3f', 'jockey', 'trainer', 'owner'
        ]

        self.new_cols = HistFeatureGenerator.generate_historical_features(
            dataset=self.dataset[calculation_cols],
            n_races=n_races, n_days=n_days
        )

        self.dataset = pd.concat(
            objs=[
                self.dataset,
                pd.DataFrame(self.new_cols)
            ], axis=1
        ).copy()
        self.dataset = self.dataset.loc[:, ~self.dataset.columns.duplicated()].copy()

        self.pipeline = self.get_preprocessing_pipeline()

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
