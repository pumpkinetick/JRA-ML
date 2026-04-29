from typing import Callable, Optional

import numpy as np


class ROICalculator:
    def __init__(self,
                 y_pred_split: list,
                 race_data_split: list
                 ):
        self.y_pred_split = y_pred_split
        self.race_data_split = race_data_split

    def run_simulation(self,
                       k: int,
                       success_fn: Callable,
                       payout_fn: Callable,
                       filter_fn: Optional[Callable] = None
                       ) -> dict:
        total_races = len(self.race_data_split)
        total_bets = 0
        total_payout = 0.0
        wins = 0

        for i, race_data in enumerate(self.race_data_split):
            preds = self.y_pred_split[i]
            if len(preds) < k:
                continue

            top_indices = np.argsort(preds)[::-1]

            if filter_fn and not filter_fn(preds, top_indices):
                continue

            total_bets += 1
            top_horses = [race_data[idx] for idx in top_indices[:k]]

            if success_fn(top_horses):
                wins += 1
                total_payout += payout_fn(top_horses, race_data)

        roi = (total_payout / total_bets * 100) if total_bets > 0 else 0.0
        win_rate = (wins / total_bets * 100) if total_bets > 0 else 0.0

        return {
            'total_bets': total_bets,
            'total_races': total_races,
            'wins': wins,
            'total_payout': total_payout,
            'roi': roi,
            'win_rate': win_rate
        }

    def calculate_flat_bet_roi(self) -> dict:
        return self.run_simulation(
            k=1,
            success_fn=lambda horses: horses[0]['fp'] == 1,
            payout_fn=lambda horses, _: horses[0].get('win_odds', 0.0)
        )

    def calculate_confidence_roi(self,
                                 conf_margin: float = 0.8
                                 ) -> dict:
        return self.run_simulation(
            k=2,
            filter_fn=lambda preds, idx: preds[idx[0]] - preds[idx[1]] > conf_margin,
            success_fn=lambda horses: horses[0]['fp'] == 1,
            payout_fn=lambda horses, _: horses[0].get('win_odds', 0.0)
        )

    def calculate_place_roi(self) -> dict:
        return self.run_simulation(
            k=1,
            success_fn=lambda horses: horses[0]['fp'] in [1, 2, 3],
            payout_fn=lambda horses, _: horses[0].get('place_1_odds', 0.0) / 100
        )

    def calculate_trio_roi(self) -> dict:
        return self.run_simulation(
            k=3,
            success_fn=lambda horses: {h['fp'] for h in horses} == {1, 2, 3},
            payout_fn=lambda _, race: race[0].get('trio_1_odds', 0.0) / 100
        )
