import lightgbm as lgb

from src.training.model_trainer import ModelTrainer


class Evaluator:
    def __init__(self,
                 model_trainer: ModelTrainer,
                 model: lgb.LGBMRanker
                 ):
        self.model = model
