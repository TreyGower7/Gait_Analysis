import logging
import pandas as pd
import requests

class ingest():
    def __init__(self, data_path:str):
        """
        Abstract Method
        """
        self.data_path = data_path

    def get_data(self) -> pd.DataFrame:
        """
        Get the data
        """
        logging.info(f"Reading data from {self.data_path}")
        try:
            response = requests.get(self.data_path)
            lines = response.text.strip().split("\n")
            #df = pd.read_csv(self.data_path)
            return response, lines
        except Exception as e:
            logging.info(f"Error ingesting data as {e}")

def get_data(data_path:str) -> pd.DataFrame:

    try:
        ingest_data = ingest(data_path)
        response, lines = ingest_data.get_data()
        return response, lines
    except Exception as e:
        logging.info(f"Error in get_data {e}")
url = "https://raw.githubusercontent.com/Vortander/KinectGait/refs/heads/master/Data/Person156/1.txt"


response, lines = get_data(url)

data = []
frame = -1

for line in lines:
    if not line.strip():
        continue
    parts = line.strip().split(";")
    joint_name = parts[0]
    x, y, z = map(float, parts[1:])

    if joint_name == "Head":
        frame += 1

    data.append({"Frame": frame, "Joint": joint_name, "X": x, "Y": y, "Z": z})

df = pd.DataFrame(data)
del data
print(df.head())