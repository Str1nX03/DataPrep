import os
import sys
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging

def save_dataset(dataset_path, output_filename = "data.csv", save_dir="artifacts" ):
    '''
    Saves a dataset (CSV) permanently in the specified directory as "data.csv".
    Returns the full path to the saved dataset.
    '''
    try:
        os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
        save_path = os.path.join(save_dir, output_filename)

        df = pd.read_csv(dataset_path)  # Read the dataset
        df.to_csv(save_path, index=False)  # Save permanently in artifacts/

        logging.info(f"Dataset saved permanently at {save_path}")
        return save_path

    except Exception as e:
        raise CustomException(e, sys)