import logging
import pandas as pd
import requests
from io import StringIO
from zenml import step
import time

class IngestData:
    def __init__(self, data_path: str = None, meta_data_url: str = None):
        self.data_path = data_path
        self.meta_data_url = meta_data_url
        self.meta_data = None
        if self.meta_data_url:
            self.meta_data = self._load_metadata()

    def _load_metadata(self) -> pd.DataFrame:
        logging.info("Loading metadata...")
        return pd.read_csv(self.meta_data_url)

    def get_data(self) -> pd.DataFrame:
        headers = ["Joint", "X", "Y", "Z"]
        response = requests.get(self.data_path)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text), sep=";", names=headers)
        df["Index"] = df.groupby("Joint").cumcount() + 1
        df["Joint"] = df["Joint"] + "_" + df["Index"].astype(str)
        df.set_index("Joint", inplace=True)
        return df

    def extract_person_id(self) -> str:
        try:
            return self.data_path.split("Data/")[1].split("/")[0]
        except Exception as e:
            logging.warning(f"Failed to extract PersonID: {e}")
            return "Unknown"

    def load_all_motion_data(self, file_count: int) -> dict:
        data_dict = {"MetaData": self.meta_data}
        headers = ["Joint", "X", "Y", "Z"]
        for i in range(file_count):
            person_id = f"Person{i+1:03d}"
            url = f"{self.data_path}/{person_id}/1.txt"

            for attempt in range(10):  # Retry up to 10 times
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    df = pd.read_csv(StringIO(response.text), sep=";", names=headers)
                    df["Index"] = df.groupby("Joint").cumcount() + 1
                    df["Joint"] = df["Joint"] + "_" + df["Index"].astype(str)
                    df.set_index("Joint", inplace=True)
                    data_dict[person_id] = df
                    logging.info(f"{person_id} loaded with {len(df)} joints")
                    break  # Success, exit retry loop
                except requests.exceptions.RequestException as e:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logging.warning(f"Attempt {attempt + 1}: Failed to load {person_id} ({e}). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
            else:
                logging.error(f"Failed to load {person_id} after 10 attempts.")

        return data_dict


def ingest_data(data_path: str, meta_data: str) -> dict:
    """
    ZenML step to ingest a single person's motion data.
    """
    ingester = IngestData(data_path=data_path, meta_data_url=meta_data)
    logging.info(f"Ingesting Data from: {data_path}")
    try:
        df = ingester.load_all_motion_data(file_count=140)
        return df
    except Exception as e:
        logging.warning(f"Data invalid or failed to ingest from {data_path}: {e}")
        return {}
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    df = ingest_data(
        data_path="https://raw.githubusercontent.com/Vortander/KinectGait/master/Data",
        meta_data="https://raw.githubusercontent.com/Vortander/KinectGait/master/GenderBMIData/person-data.csv?raw=true"
    )
    print(f"Loaded {len(df) - 1} people + metadata.")
    print(df.keys())