import lightgbm as lgb
import numpy as np
import pandas as pd

from training.model_trainer import ModelTrainer


class Evaluator:
    def __init__(self,
                 model_trainer: ModelTrainer,
                 model: lgb.LGBMRanker
                 ):
        self.model_trainer = model_trainer
        self.model = model

        test_scores = self.model.predict(X=self.model_trainer.X_test)
        self.y_true_split = self.split_by_group(
            arr=self.model_trainer.y_test,
            groups=self.model_trainer.test_groups
        )
        self.y_pred_split = self.split_by_group(
            arr=test_scores,
            groups=self.model_trainer.test_groups
        )

        self.print_score()
        self.print_importance()

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

    def print_score(self):
        for k in [1, 3, 5]:
            score = self.ndcg_at_k(
                y_true_groups=self.y_true_split,
                y_pred_groups=self.y_pred_split,
                k=k
            )
            print(f'NDCG@{k}: {score:.4f}')

        winner_accuracy = sum(
            y_true[np.argmax(y_pred)] == max(y_true)
            for y_true, y_pred in zip(self.y_true_split, self.y_pred_split)
        )
        print(
            f'Winner correctly predicted: {winner_accuracy}/{len(self.model_trainer.test_groups)} '
            f'({100*winner_accuracy/len(self.model_trainer.test_groups):.1f}%)\n'
        )

    def print_importance(self):
        feature_names = self.model_trainer.pipeline.get_feature_names_out()
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values(by='importance', ascending=False)

        for row in importance_df.iterrows():
            print(f'{row[1]["feature"]}: {row[1]["importance"]:.4f}')

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
