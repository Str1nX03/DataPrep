import os
import sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class DataPreProcessConfig:
    data_path: str = os.path.join("artifacts", "preprocessed_data.csv")

class DataPreProcess:
    def __init__(self):
        self.pre_process_config = DataPreProcessConfig()

    def initiate_data_pre_processing(self):
        logging.info("Entered the data processing zone.")
        df = pd.read_csv("artifacts/data.csv")