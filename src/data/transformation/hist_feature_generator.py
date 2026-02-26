import numpy as np
import pandas as pd


class HistFeatureGenerator:
    @staticmethod
    def generate_historical_features(dataset: pd.DataFrame,
                                     n_races: int = 5,
                                     n_days: int = 180
                                     ) -> dict:
        new_cols = dict()

        is_winner_series = pd.Series((dataset['fp'] == 1) * 1)
        horse_grouping = dataset.groupby(
            by='horse_name',
            observed=True, sort=False
        )

        new_cols['horse_race_count'] = (
            horse_grouping.cumcount()
        )

        for surface in ['Turf', 'Dirt']:
            mask = (dataset['turf_or_dirt'] == surface)
            surface_fp = dataset['fp'].where(mask)
            col_name = f'horse_avg_fp_{surface.lower()}'
            new_cols[col_name] = (
                surface_fp.groupby(by=dataset['horse_name'], observed=True, sort=False)
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

        new_cols['horse_avg_fp'] = get_avg_horse_data(target_col='fp')
        new_cols['horse_avg_l3f'] = get_avg_horse_data(target_col='l3f')

        new_cols['days_since_last'] = (
            horse_grouping['race_date']
            .diff().dt.days
        )

        new_cols['horse_win_rate'] = (
            is_winner_series.groupby(
                by=dataset['horse_name'],
                observed=True, sort=False
            )
            .rolling(window=n_races).mean()
            .reset_index(level=0, drop=True)
            .shift(1).values
        )
        for col in ['jockey', 'trainer', 'owner']:
            temp = dataset[[col, 'race_date']].copy()
            temp['is_winner'] = is_winner_series.values

            new_cols[f'{col}_win_rate'] = (
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

        return new_cols
