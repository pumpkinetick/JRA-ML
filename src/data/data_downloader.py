import gdown


class DataDownloader:
    def __init__(self,
                 drive_link: str,
                 data_path: str = None
                 ):
        self.drive_link = drive_link
        self.data_path = data_path

        if self.data_path is None:
            self.data_path = 'data'

        self.download_data()

    def download_data(self):
        gdown.download_folder(
            url=self.drive_link,
            output=self.data_path
        )
