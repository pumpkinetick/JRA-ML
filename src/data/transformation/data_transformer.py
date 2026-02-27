import pandas as pd

from src.data.preparation.data_translator import DataTranslator


class DataTransformer:
    def __init__(self,
                 data_translator: DataTranslator
                 ):
        self.dataset = self.merge_data(data_translator=data_translator)

        self.clean_dataset()

    @staticmethod
    def merge_data(data_translator: DataTranslator
                   ) -> pd.DataFrame:
        merged_data = (
            data_translator.race_results.merge(
                data_translator.corner_passing_orders,
                on='race_id', how='left'
            ).merge(
                data_translator.laptimes,
                on='race_id', how='left'
            ).merge(
                data_translator.odds,
                on='race_id', how='left'
            )
        )
        return merged_data

    def clean_dataset(self):
        self.dataset['race_date'] = pd.to_datetime(self.dataset['race_date'])
        self.dataset = self.dataset.sort_values(by=['race_date', 'race_id', 'pp'], kind='mergesort')
        self.dataset.dropna(subset=['fp'], inplace=True)
        self.dataset['track_direction'] = self.dataset['track_direction'].fillna('Straight')
        self.dataset.reset_index(drop=True, inplace=True)
