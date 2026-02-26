import numpy as np


class ROICalculator:
    @staticmethod
    def calculate_flat_bet_roi(y_pred_split: list,
                               race_data_split: list
                               ):
        total_races = len(race_data_split)

        total_payout = 0.0
        wins = 0
        for i, race_data in enumerate(race_data_split):
            pred_winner_idx = np.argmax(y_pred_split[i])
            chosen_horse = race_data[pred_winner_idx]
            if chosen_horse['fp'] == 1:
                total_payout += chosen_horse['win_odds']
                wins += 1

        roi = (total_payout / total_races) * 100
        print(f'--- Flat Betting Strategy (#1 Pick) ---')
        print(f'Total Bets: {total_races} | Wins: {wins}')
        print(f'Total Payout: {total_payout:.2f} | ROI: {roi:.2f}%')
        print(f'Win Rate: {(wins / total_races) * 100:.2f}%\n')

    @staticmethod
    def calculate_confidence_roi(y_pred_split: list,
                                 race_data_split: list,
                                 conf_margin: float = 0.8
                                 ):
        total_bets = 0
        total_payout = 0.0
        for i, race_data in enumerate(race_data_split):
            preds = y_pred_split[i]
            if len(preds) < 2:
                continue

            top_indices = np.argsort(preds)[::-1]
            score_diff = preds[top_indices[0]] - preds[top_indices[1]]
            if score_diff > conf_margin:
                total_bets += 1
                chosen_horse = race_data[top_indices[0]]
                if chosen_horse['fp'] == 1:
                    total_payout += chosen_horse['win_odds']

        print(f'--- Confidence Strategy (Margin > {conf_margin}) ---')

        if total_bets == 0:
            print('No bets met the confidence threshold.\n')

        roi = (total_payout / total_bets) * 100
        print(f'Total Bets: {total_bets} (out of {len(race_data_split)} races)')
        print(f'Total Payout: {total_payout:.2f} | ROI: {roi:.2f}%\n')
