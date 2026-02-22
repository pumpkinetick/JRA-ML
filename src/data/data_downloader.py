from pathlib import Path

import gdown

from src import PROJECT_PATH


class DataDownloader:
    def __init__(self,
                 drive_link: str,
                 data_path: Path = None
                 ):
        self.drive_link = drive_link
        self.data_path = data_path

        if self.data_path is None:
            self.data_path = PROJECT_PATH / 'data'

        self.download_data()

    def download_data(self):
        gdown.download_folder(
            url=self.drive_link,
            output=str(self.data_path)
        )
