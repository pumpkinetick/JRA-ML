import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


class TrainingDataPreparer:
    def __init__(self,
                 dataset: pd.DataFrame,
                 numerical_features: list,
                 categorical_features: list,
                 ordinal_features: list,
                 ordinal_categories: list,
                 historical_features: list,
                 split_date: str
                 ):
        self.dataset = dataset
        self.split_date = pd.to_datetime(split_date)

        self.train_df = pd.DataFrame()
        self.X_train = pd.DataFrame()
        self.y_train = np.ndarray((0, 0))
        self.train_groups = np.ndarray((0, 0))

        self.test_df = pd.DataFrame()
        self.X_test = pd.DataFrame()
        self.y_test = np.ndarray((0, 0))
        self.test_groups = np.ndarray((0, 0))

        self.pipeline = self.get_preprocessing_pipeline(
            numerical_features=numerical_features,
            categorical_features=categorical_features,
            ordinal_features=ordinal_features,
            ordinal_categories=ordinal_categories,
            historical_features=historical_features
        )

        self.prepare_training_data()
        self.prepare_test_data()

    @staticmethod
    def get_preprocessing_pipeline(numerical_features: list,
                                   categorical_features: list,
                                   ordinal_features: list,
                                   ordinal_categories: list,
                                   historical_features: list
                                   ) -> ColumnTransformer:
        column_transformer = ColumnTransformer(
            transformers=[
                ('num', Pipeline([
                    ('impute', SimpleImputer(strategy='median')),
                    ('scale', StandardScaler())
                ]), numerical_features),

                ('hist', Pipeline([
                    ('impute', SimpleImputer(strategy='constant', fill_value=-1)),
                    ('scale', StandardScaler())
                ]), historical_features),

                ('cat', Pipeline([
                    ('impute', SimpleImputer(strategy='most_frequent')),
                    ('ord', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
                ]), categorical_features),

                ('ord', OrdinalEncoder(
                    categories=ordinal_categories,
                    handle_unknown='use_encoded_value',
                    unknown_value=-1
                ), ordinal_features)
            ],
            remainder='drop'
        )
        column_transformer.set_output(transform='pandas')
        return column_transformer

    def prepare_training_data(self):
        self.train_df = self.dataset[self.dataset['race_date'] < self.split_date]

        self.train_groups = self.train_df.groupby(by='race_id', sort=True).size().values

        self.X_train = self.pipeline.fit_transform(self.train_df)
        self.y_train = self.make_relevance(
            fp_array=self.train_df['fp'].values, group_sizes=self.train_groups
        )

    def prepare_test_data(self):
        self.test_df = self.dataset[self.dataset['race_date'] >= self.split_date]

        self.test_groups = self.test_df.groupby(by='race_id', sort=True).size().values

        self.X_test = self.pipeline.transform(self.test_df)
        self.y_test = self.make_relevance(
            fp_array=self.test_df['fp'].values, group_sizes=self.test_groups
        )

    @staticmethod
    def make_relevance(fp_array: np.ndarray,
                       group_sizes: np.ndarray
                       ) -> np.ndarray:
        rel = np.zeros(len(fp_array), dtype=np.int32)
        idx = 0
        for size in group_sizes:
            fp = fp_array[idx:idx + size]
            r = rel[idx:idx + size]
            r[fp == 1] = 3
            r[fp == 2] = 2
            r[fp == 3] = 2
            r[fp == 4] = 1
            r[fp == 5] = 1
            idx += size
        return rel
