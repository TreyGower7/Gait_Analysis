import logging
from abc import ABC, abstractmethod
from typing import Annotated, Tuple, Union, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from random import shuffle



# Abstract class for data strategy
class DataStrategy(ABC):

    @abstractmethod
    def handle_data(self, data: pd.DataFrame) -> Any:
        """
        Abstract method to handle data cleaning.
        """
        pass
        

class DataPreProcess(DataStrategy):
    """
    Data Preprocessing class to handle data preprocessing.
    """
    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Handles data preprocessing.
        """

        if data is None:
            logging.error("Data is None")
            raise ValueError("Data is None")
        if not isinstance(data, pd.DataFrame):
            logging.error("Data is not a DataFrame")
            raise ValueError("Data is not a DataFrame")
        else:
            try:
                
                
                
                return super().handle_data(data)
            except ImportError as e:
                logging.error(f"Error importing libraries: {e}")
                raise e
    

class DataDivideStrategy(DataStrategy):
    """
    Split data into train, test, and validation sets for CNN.
    """
    def handle_data(self, data):
        try:
            # Define some independent and dependant variable/variables
            X = data.drop("order_status", axis=1)
            Y = data["order_status"]
            # Split data into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(data, test_size=0.2, random_state=42)
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error(f"Error in splitting data: {e}")
            raise e
        
# class DataDivideImageStrategy(DataStrategy):
#     """
#     Split data into train, test, and validation sets for images.
#     """
#     def handle_data(self, data):
#         try:
#             split_ratio_train = 0.7  # 70% train
#             split_ratio_val = 0.15  # 15% validation (from train data)
#             split_ratio_test = 0.15  # 15% test
#             # Split data into test and validation sets
#             train_val_data, test_data = train_test_split(data, test_size=split_ratio_test, random_state=42)
#             # Further split the train data into train and validation sets
#             rel_val_ratio = split_ratio_val / (split_ratio_train + split_ratio_val)
#             train_data, val_data = train_test_split(train_val_data, test_size=rel_val_ratio, random_state=42)
#             return train_data, test_data, val_data
#         except Exception as e:
#             logging.error(f"Error in splitting image data: {e}")
#             raise e
        
class DataCleaning():
    """
    Class to handle data cleaning.
    """
    def __init__(self, data: pd.DataFrame, strategy: DataStrategy):
        self.data = data
        self.strategy = strategy

    def handle_data(self) -> any:
        """
        Handles data
        """
        try:
            self.strategy.handle_data(self.data)
            return self.data
        except Exception as e:
            logging.error(f"Error in cleaning data: {e}")
            raise e
        