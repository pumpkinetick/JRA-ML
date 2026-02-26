import numpy as np
import pandas as pd

from data.transformation.data_analyzer import DataAnalyzer


class TrainingDataPreparer:
    def __init__(self,
                 data_analyzer: DataAnalyzer,
                 split_date: str
                 ):
        self.dataset = data_analyzer.dataset
        self.pipeline = data_analyzer.pipeline
        self.split_date = pd.to_datetime(split_date)

        self.train_df = pd.DataFrame()
        self.X_train = pd.DataFrame()
        self.y_train = np.ndarray((0, 0))
        self.train_groups = np.ndarray((0, 0))

        self.test_df = pd.DataFrame()
        self.X_test = pd.DataFrame()
        self.y_test = np.ndarray((0, 0))
        self.test_groups = np.ndarray((0, 0))

        self.prepare_training_data()
        self.prepare_test_data()

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
