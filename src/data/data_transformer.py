import pandas as pd

from src.data.data_translator import DataTranslator


class DataTransformer:
    @staticmethod
    def merge_data(data_translator: DataTranslator
                   ) -> pd.DataFrame:
        merged_data = data_translator.race_results

        merged_data = merged_data.merge(
            data_translator.corner_passing_orders,
            on='race_id', how='left'
        )
        merged_data = merged_data.merge(
            data_translator.laptimes,
            on='race_id', how='left'
        )
        merged_data = merged_data.merge(
            data_translator.odds,
            on='race_id', how='left'
        )

        return merged_data
