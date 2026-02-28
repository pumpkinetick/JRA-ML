from typing import Callable

import numpy as np


class ROICalculator:
    def __init__(self,
                 y_pred_split: list,
                 race_data_split: list
                 ):
        self.y_pred_split = y_pred_split
        self.race_data_split = race_data_split

    def run_simulation(self,
                       name: str,
                       k: int,
                       success_fn: Callable,
                       payout_fn: Callable,
                       filter_fn: Callable = None
                       ):
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

        self.print_results(
            name=name,
            total_bets=total_bets,
            total_races=total_races,
            wins=wins,
            total_payout=total_payout
        )

    @staticmethod
    def print_results(name: str,
                      total_bets: int,
                      total_races: int,
                      wins: int,
                      total_payout: float
                      ):
        print(f'--- {name} ---')
        if total_bets == 0:
            print("No bets met the criteria.\n")
            return

        roi = (total_payout / total_bets) * 100
        win_rate = (wins / total_bets) * 100
        print(f'Total Bets: {total_bets} (out of {total_races} races) | Wins: {wins}')
        print(f'Total Payout: {total_payout:.1f} | ROI: {roi:.2f}% | Win Rate: {win_rate:.2f}%\n')

    def calculate_flat_bet_roi(self):
        self.run_simulation(
            name='Flat Betting Strategy (#1 Pick)',
            k=1,
            success_fn=lambda horses: horses[0]['fp'] == 1,
            payout_fn=lambda horses, _: horses[0].get('win_odds', 0.0)
        )

    def calculate_confidence_roi(self, conf_margin: float = 0.8):
        self.run_simulation(
            name=f'Confidence Strategy (Margin > {conf_margin})',
            k=2,
            filter_fn=lambda preds, idx: preds[idx[0]] - preds[idx[1]] > conf_margin,
            success_fn=lambda horses: horses[0]['fp'] == 1,
            payout_fn=lambda horses, _: horses[0].get('win_odds', 0.0)
        )

    def calculate_place_roi(self):
        self.run_simulation(
            name='Place Strategy (Top 1 finishes in Top 3)',
            k=1,
            success_fn=lambda horses: horses[0]['fp'] in [1, 2, 3],
            payout_fn=lambda horses, _: horses[0].get('place_1_odds', 0.0)
        )

    def calculate_trio_roi(self):
        self.run_simulation(
            name='Trio Strategy (Top 3 are 1st, 2nd, 3rd)',
            k=3,
            success_fn=lambda horses: {h['fp'] for h in horses} == {1, 2, 3},
            payout_fn=lambda _, race: race[0].get('trio_1_odds', 0.0)
        )
