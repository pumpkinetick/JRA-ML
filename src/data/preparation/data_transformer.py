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
            if 'Newcomer' in cond:
                return 'Newcomer'
            if 'Maiden' in cond:
                return 'Maiden'
            for wins in [1, 2, 3]:
                if f'{wins}-win' in cond:
                    return f'{wins}-win'
            if 'Under ' in cond:
                return cond.split('Under ')[1]
            if 'Open' in cond:
                return 'Open'
            return 'Other'

        def get_age_limit(cond: str
                          ) -> str:
            for age in [2, 3, 4, 5]:
                if f'{age}yo' in cond and '+' not in cond:
                    return f'{age}yo'
                if f'{age}yo+' in cond:
                    return f'{age}yo_up'
            return 'Other'

        new_cols['race_class'] = self.dataset['race_cond'].apply(get_class)
        new_cols['race_age_limit'] = self.dataset['race_cond'].apply(get_age_limit)

        self.dataset.drop(columns=['race_cond'], inplace=True)
        self.dataset = pd.concat(
            objs=[
                self.dataset,
                pd.DataFrame(new_cols)
            ], axis=1
        ).copy()
        self.dataset = self.dataset.loc[:, ~self.dataset.columns.duplicated()].copy()
