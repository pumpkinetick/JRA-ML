import lightgbm as lgb

from training.training_data_preparer import TrainingDataPreparer


class ModelTrainer:
    def __init__(self,
                 training_data_preparer: TrainingDataPreparer,
                 ):
        self.X_train = training_data_preparer.X_train
        self.y_train = training_data_preparer.y_train
        self.train_groups = training_data_preparer.train_groups

        self.X_test = training_data_preparer.X_test
        self.y_test = training_data_preparer.y_test
        self.test_groups = training_data_preparer.test_groups

        self.pipeline = training_data_preparer.pipeline

    def fit_model(self,
                  training_args: dict,
                  fit_args: dict
                  ) -> lgb.LGBMRanker:
        model = lgb.LGBMRanker(**training_args)

        model.fit(
            self.X_train, self.y_train,
            group=self.train_groups,
            eval_set=[(self.X_test, self.y_test)],
            eval_group=[self.test_groups],
            **fit_args
        )

        return model
