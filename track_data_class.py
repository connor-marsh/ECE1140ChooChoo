
import pandas as pd

class TrackDataClass():
    def __init__(self, filepath: str):
        """
        Initialization for the static track data.

        :param filepath: The filepath to an excel containing information about the track
        """
        self.file_data = pd.read_excel(filepath)
