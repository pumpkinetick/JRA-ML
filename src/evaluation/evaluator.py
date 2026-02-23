import lightgbm as lgb
import numpy as np

from src.training.model_trainer import ModelTrainer


class Evaluator:
    def __init__(self,
                 model_trainer: ModelTrainer,
                 model: lgb.LGBMRanker
                 ):
        self.model = model
        test_scores = self.model.predict(X=model_trainer.X_test)

        self.y_true_split = self.split_by_group(
            arr=model_trainer.y_test,
            groups=model_trainer.test_groups
        )
        self.y_pred_split = self.split_by_group(
            arr=test_scores,
            groups=model_trainer.test_groups
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
