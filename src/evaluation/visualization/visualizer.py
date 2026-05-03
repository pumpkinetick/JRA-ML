import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Visualizer:
    @staticmethod
    def plot_ndcg(ndcg_stats: dict):
        data = pd.DataFrame({
            'k': list(ndcg_stats.keys()),
            'NDCG': list(ndcg_stats.values())
        })

        plt.figure(figsize=(10, 6))
        sns.barplot(data=data, x='k', y='NDCG', palette='viridis', hue='k', legend=False)
        plt.title('NDCG@k Scores')
        plt.ylim(0, 1)
        plt.show()

    @staticmethod
    def plot_importance(importance_df: pd.DataFrame):
        plt.figure(figsize=(10, 8))
        sns.barplot(
            data=importance_df.sort_values(by='importance', ascending=False),
            x='importance',
            y='feature',
            palette='magma',
            hue='feature',
            legend=False
        )
        plt.title('Feature Importance')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_roi_over_time(cumulative_stats: dict):
        plt.figure(figsize=(12, 8))
        for strategy, data in cumulative_stats.items():
            sns.lineplot(x=data['years'], y=data['roi'], label=strategy)
        plt.title('Cumulative ROI Over Time')
        plt.xlabel('Year')
        plt.ylabel('ROI (%)')
        plt.legend()
        plt.grid(True)
        plt.show()
