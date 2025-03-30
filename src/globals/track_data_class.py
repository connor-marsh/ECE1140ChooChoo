
import pandas as pd

class TrackDataClass():
    def __init__(self, filepath: str):
        """
        Initialization for the static track data.

        :param filepath: The filepath to an excel containing information about the track
        """
        file_data = pd.read_excel(filepath)
        self.blocks = self.read_output(file_data)

    def read_output(self, file_data: dict):
        """
        Takes the output pandas dictionary from the excel file and converts it to a more usable form

        :param file_data: A dictionary containing the output from the track definition excel sheet

        :return :

        """

        
        
