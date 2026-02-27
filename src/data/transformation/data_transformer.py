import pandas as pd

from src.data.preparation.data_translator import DataTranslator


class DataTransformer:
    def __init__(self,
                 data_translator: DataTranslator
                 ):
        self.dataset = self.merge_data(data_translator=data_translator)

        self.clean_dataset()
        self.parse_race_cond()

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

    def parse_race_cond(self):
        new_cols = dict()

        def get_class(cond: str
                      ) -> str:
            if any(g in cond for g in ['G1', 'G2', 'G3', 'Open', 'L']):
                return 'Open'
            if '16M' in cond or '3-win' in cond:
                return '3-win'
            if '10M' in cond or '2-win' in cond:
                return '2-win'
            if '5M' in cond or '1-win' in cond:
                return '1-win'
            if 'Maiden' in cond:
                return 'Maiden'
            if 'Newcomer' in cond:
                return 'Newcomer'
            return 'Other'

        def get_age_limit(cond: str
                          ) -> str:
            if '2yo' in cond:
                return '2yo'
            if '3yo' in cond and '+' not in cond:
                return '3yo'
            if '3yo+' in cond:
                return '3yo_up'
            if '4yo+' in cond:
                return '4yo_up'
            return 'Mixed'

        new_cols['race_class_rank'] = self.dataset['race_cond'].apply(get_class)
        new_cols['race_age_limit'] = self.dataset['race_cond'].apply(get_age_limit)

        self.dataset.drop(columns=['race_cond'], inplace=True)
        self.dataset = pd.concat(
            objs=[
                self.dataset,
                pd.DataFrame(new_cols)
            ], axis=1
        ).copy()
        self.dataset = self.dataset.loc[:, ~self.dataset.columns.duplicated()].copy()
