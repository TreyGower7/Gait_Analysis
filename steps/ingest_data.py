import logging
import pandas as pd
import requests
from zenml import step

class IngestData:
    def __init__(self, data_path: str, metadata_path: str = None):
        self.data_path = data_path
        self.metadata_path = metadata_path

    def fetch_raw_lines(self):
        response = requests.get(self.data_path)
        return response.text.strip().split("\n")

    def get_data(self, mode: str = "csv") -> pd.DataFrame:
        if mode == "csv":
            return pd.read_csv(self.data_path)

        elif mode == "raw_txt":
            lines = self.fetch_raw_lines()
            frame = -1
            data = []

            for line in lines:
                if not line.strip():
                    continue
                parts = line.strip().split(";")
                joint = parts[0]
                x, y, z = map(float, parts[1:])
                if joint == "Head":
                    frame += 1
                data.append({"Frame": frame, "Joint": joint, "X": x, "Y": y, "Z": z})

            person_id = self.extract_person_id()
            df["Individual"] = person_id  # match metadata key
            
            if self.metadata_path:
                meta = pd.read_csv(self.metadata_path)
                df = df.merge(meta, on="PersonID", how="left")
            
            return df
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def extract_person_id(self):
        try:
            return self.data_path.split("Data/")[1].split("/")[0]
        except:
            logging.warning("Failed to extract PersonID")
            return "Unknown"
