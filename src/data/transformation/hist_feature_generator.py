import numpy as np
import pandas as pd


class HistFeatureGenerator:
    @staticmethod
    def generate_historical_features(dataset: pd.DataFrame,
                                     n_races: int = 5,
                                     n_days: int = 180
                                     ) -> dict:
        new_cols = dict()

        df_temp = dataset.copy()
        df_temp['is_winner'] = (df_temp['fp'] == 1) * 1

        horse_grouping = df_temp.groupby(by='horse_name', observed=True, sort=False)

        new_cols['horse_race_count'] = horse_grouping.cumcount()

        for surface in ['Turf', 'Dirt']:
            col_name = f'horse_avg_fp_{surface.lower()}'

            only_surface = df_temp[df_temp['turf_or_dirt'] == surface]
            surface_stats = (
                only_surface.groupby(by='horse_name', observed=True, sort=False)['fp']
                .rolling(window=n_races, min_periods=1).mean()
                .groupby(by='horse_name', observed=True, sort=False).shift(1)
                .reset_index(level=0, drop=True)
                .fillna(0.0)
            )

            new_cols[col_name] = pd.Series(index=df_temp.index, data=np.nan)
            new_cols[col_name].update(surface_stats)

            new_cols[col_name] = new_cols[col_name].groupby(df_temp['horse_name']).ffill()

        def get_rel_rolling(target_col: str,
                            window: int
                            ) -> pd.Series:
            return (
                horse_grouping[target_col]
                .rolling(window=window, min_periods=1).mean()
                .reset_index(level=0, drop=True)
                .sort_index()
                .shift(1)
            )

        new_cols['horse_avg_fp'] = get_rel_rolling(target_col='fp', window=n_races)
        new_cols['horse_avg_l3f'] = get_rel_rolling(target_col='l3f', window=n_races)
        new_cols['horse_win_rate'] = get_rel_rolling(target_col='is_winner', window=n_races)

        short_fp = get_rel_rolling(target_col='fp', window=-(n_races // -2))
        new_cols['horse_fp_momentum'] = new_cols['horse_avg_fp'] - short_fp

        avg_weight = get_rel_rolling(target_col='horse_weight', window=n_races * 2)
        new_cols['horse_weight_dev_avg'] = dataset['horse_weight'] - avg_weight

        days_diff = pd.Series(horse_grouping['race_date'].diff().dt.days)
        new_cols['days_since_last'] = days_diff.fillna(999)

        def calc_human_rate(group: pd.DataFrame
                            ) -> pd.Series:
            res = group.set_index('race_date')['is_winner'].rolling(
                window=f'{n_days}D', closed='left'
            ).mean()
            res.index = group.index
            return res

        for col in ['jockey', 'trainer', 'owner']:
            new_cols[f'{col}_win_rate'] = (
                df_temp.groupby(col, observed=True, sort=False, group_keys=False)
                .apply(calc_human_rate)
                .sort_index()
                .fillna(0.0)
            )

        return new_cols
