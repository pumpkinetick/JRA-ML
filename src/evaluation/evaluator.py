from collections import defaultdict

import lightgbm as lgb
import numpy as np
import pandas as pd

from src.evaluation.roi_calculator import ROICalculator
from src.training.model_trainer import ModelTrainer


class Evaluator:
    def __init__(self,
                 model_trainer: ModelTrainer,
                 model: lgb.LGBMRanker,
                 test_df: pd.DataFrame
                 ):
        self.model = model
        self.test_groups = model_trainer.test_groups
        self.pipeline = model_trainer.pipeline

        test_scores = self.model.predict(X=model_trainer.X_test)

        self.y_true_split = self.split_by_group(
            arr=model_trainer.y_test,
            groups=self.test_groups
        )
        self.y_pred_split = self.split_by_group(
            arr=test_scores,
            groups=self.test_groups
        )

        self.race_data_split = self.split_by_group(
            arr=np.array(test_df.to_dict('records')),
            groups=self.test_groups
        )

    @staticmethod
    def split_by_group(arr: np.ndarray,
                       groups: np.ndarray
                       ) -> list:
        splits = list()
        idx = 0
        for size in groups:
            splits.append(arr[idx:idx + size])
            idx += size
        return splits

    def get_ndcg_stats(self,
                       k_list: list[int] = None
                       ) -> dict:
        if k_list is None:
            k_list = [1, 3, 5]
        stats = dict()
        for k in k_list:
            score = self.ndcg_at_k(
                y_true_groups=self.y_true_split,
                y_pred_groups=self.y_pred_split,
                k=k
            )
            stats[f'NDCG@{k}'] = score
        return stats

    def get_roi_stats(self,
                      conf_margin: float
                      ) -> dict:
        roi_calculator = ROICalculator(
            y_pred_split=self.y_pred_split,
            race_data_split=self.race_data_split
        )
        return {
            'Flat Bet': roi_calculator.calculate_flat_bet_roi(),
            f'Confidence (Margin > {conf_margin})': (
                roi_calculator.calculate_confidence_roi(conf_margin=conf_margin)
            ),
            'Place': roi_calculator.calculate_place_roi(),
            'Trio': roi_calculator.calculate_trio_roi()
        }

    def get_importance_stats(self) -> pd.DataFrame:
        feature_names = self.pipeline.get_feature_names_out()
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values(by='importance', ascending=False)
        return importance_df

    @staticmethod
    def ndcg_at_k(y_true_groups: list,
                  y_pred_groups: list,
                  k: int
                  ) -> float:
        scores = list()
        discounts = np.log2(np.arange(2, k + 2))

        def calculate_dcg(gains: np.ndarray
                          ) -> float:
            n = len(gains)
            numerator = np.subtract(np.power(2.0, gains), 1.0)
            return np.sum(np.divide(numerator, discounts[:n]))

        for y_true, y_pred in zip(y_true_groups, y_pred_groups):
            pred_order = np.argsort(y_pred)[::-1][:k]
            dcg = calculate_dcg(gains=y_true[pred_order])

            ideal_gains = np.sort(y_true)[::-1][:k]
            idcg = calculate_dcg(gains=ideal_gains)

            scores.append(dcg / idcg if idcg > 0 else 0.0)
        return float(np.mean(scores))

    def get_roi_time_series(self,
                            conf_margin: float
                            ) -> dict:
        year_indices = defaultdict(list)
        for i, race in enumerate(self.race_data_split):
            year = pd.to_datetime(race[0]['race_date']).year
            year_indices[year].append(i)

        years = sorted(year_indices.keys())

        strategies = {
            'Flat Bet': 'flat',
            f'Confidence (Margin > {conf_margin})': 'confidence',
            'Place': 'place',
            'Trio': 'trio'
        }

        cumulative_stats = dict()
        for strategy_name, strategy_key in strategies.items():
            cumulative_bets = 0
            cumulative_payout = 0.0

            roi_over_time = list()
            for year in years:
                indices = year_indices[year]
                subset_y_pred = [self.y_pred_split[i] for i in indices]
                subset_race = [self.race_data_split[i] for i in indices]

                roi_calc = ROICalculator(
                    y_pred_split=subset_y_pred,
                    race_data_split=subset_race
                )

                stats = dict()
                match strategy_key:
                    case 'flat':
                        stats = roi_calc.calculate_flat_bet_roi()
                    case 'confidence':
                        stats = roi_calc.calculate_confidence_roi(conf_margin=conf_margin)
                    case 'place':
                        stats = roi_calc.calculate_place_roi()
                    case 'trio':
                        stats = roi_calc.calculate_trio_roi()

                cumulative_bets += stats['total_bets']
                cumulative_payout += stats['total_payout']

                roi = (cumulative_payout / cumulative_bets * 100) if cumulative_bets > 0 else 0.0
                roi_over_time.append(roi)

            cumulative_stats[strategy_name] = {'years': years, 'roi': roi_over_time}

        return cumulative_stats
