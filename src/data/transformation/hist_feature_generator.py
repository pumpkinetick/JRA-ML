import numpy as np
import pandas as pd


class HistFeatureGenerator:
    @staticmethod
    def generate_historical_features(dataset: pd.DataFrame,
                                     n_races: int = 5,
                                     n_days: int = 180
                                     ) -> dict:
        historical_features = dict()

        df_temp = dataset.copy()
        df_temp['is_winner'] = (df_temp['fp'] == 1) * 1

        horse_grouping = df_temp.groupby(by='horse_name', observed=True, sort=False)

        historical_features['horse_race_count'] = horse_grouping.cumcount()

        surf_stats = dict()
        for surface in ['Turf', 'Dirt']:
            only_surface = df_temp[df_temp['turf_or_dirt'] == surface]

            s_series = (
                only_surface.groupby(by='horse_name', observed=True, sort=False)['fp']
                .rolling(window=n_races, min_periods=1).mean()
                .groupby(by='horse_name', observed=True, sort=False).shift(1)
                .reset_index(level=0, drop=True)
                .sort_index()
            )

            full_series = pd.Series(index=df_temp.index, data=np.nan)
            full_series.update(s_series)
            surf_stats[surface] = full_series.groupby(df_temp['horse_name']).ffill()

        historical_features['horse_avg_fp_target_surf'] = np.where(
            df_temp['turf_or_dirt'] == 'Turf',
            surf_stats['Turf'],
            surf_stats['Dirt']
        )
        historical_features['horse_avg_fp_other_surf'] = np.where(
            df_temp['turf_or_dirt'] == 'Turf',
            surf_stats['Dirt'],
            surf_stats['Turf']
        )

        def get_rel_rolling(target_col: str,
                            window: int
                            ) -> pd.Series:
            return (
                horse_grouping[target_col]
                .rolling(window=window, min_periods=1).mean()
                .groupby(by='horse_name', observed=True, sort=False).shift(1)
                .reset_index(level=0, drop=True)
                .sort_index()
            )

        historical_features['horse_avg_fp'] = get_rel_rolling(target_col='fp', window=n_races)
        historical_features['horse_avg_l3f'] = get_rel_rolling(target_col='l3f', window=n_races)
        historical_features['horse_win_rate'] = get_rel_rolling(target_col='is_winner', window=n_races)

        short_fp = get_rel_rolling(target_col='fp', window=-(n_races // -2))
        historical_features['horse_fp_momentum'] = short_fp - historical_features['horse_avg_fp']

        avg_weight = get_rel_rolling(target_col='horse_weight', window=n_races * 2)
        historical_features['horse_weight_dev_avg'] = dataset['horse_weight'] - avg_weight

        days_diff = pd.Series(horse_grouping['race_date'].diff().dt.days)
        historical_features['days_since_last'] = days_diff.fillna(999)

        def calc_human_rate(group: pd.DataFrame
                            ) -> pd.Series:
            res = group.set_index('race_date')['is_winner'].rolling(
                window=f'{n_days}D', closed='left'
            ).mean()
            res.index = group.index
            return res

        for col in ['jockey', 'trainer', 'owner']:
            historical_features[f'{col}_win_rate'] = (
                df_temp.groupby(col, observed=True, sort=False, group_keys=False)
                .apply(calc_human_rate)
                .sort_index()
            )

        return historical_features
