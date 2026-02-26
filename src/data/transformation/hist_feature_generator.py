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

        new_cols['horse_race_count'] = horse_grouping.cumcount()
        new_cols['is_first_race'] = (new_cols['horse_race_count'] == 0) * 1

        for surface in ['Turf', 'Dirt']:
            mask = (dataset['turf_or_dirt'] == surface)
            surface_fp = dataset['fp'].where(mask)
            col_name = f'horse_avg_fp_{surface.lower()}'
            new_cols[col_name] = (
                surface_fp.groupby(by=dataset['horse_name'], observed=True, sort=False)
                .rolling(window=n_races, min_periods=1).mean()
                .reset_index(level=0, drop=True).shift(1).values
            )

        def get_rel_rolling(target_col: str,
                            window: int
                            ) -> np.ndarray:
            return (
                horse_grouping[target_col]
                .rolling(window=window, min_periods=1).mean()
                .reset_index(level=0, drop=True)
                .shift(1).values
            )

        new_cols['horse_avg_fp'] = get_rel_rolling(target_col='fp', window=n_races)
        new_cols['horse_avg_l3f'] = get_rel_rolling(target_col='l3f', window=n_races)

        new_cols['horse_win_rate'] = (
            is_winner_series.groupby(
                by=dataset['horse_name'],
                observed=True, sort=False
            )
            .rolling(window=n_races).mean()
            .reset_index(level=0, drop=True)
            .shift(1).values
        )

        short_fp = get_rel_rolling(target_col='fp', window=-(n_races // -2))
        new_cols['horse_fp_momentum'] = new_cols['horse_avg_fp'] - short_fp

        avg_weight = get_rel_rolling(target_col='horse_weight', window=n_races * 2)
        new_cols['horse_weight_dev_avg'] = dataset['horse_weight'] - avg_weight

        days_diff = pd.Series(horse_grouping['race_date'].diff().dt.days)
        new_cols['days_since_last'] = days_diff.fillna(999)

        new_cols['is_layoff'] = (new_cols['days_since_last'] > 90) * 1

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
