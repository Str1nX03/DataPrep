import os
import sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from pathlib import Path

@dataclass
class DataPreProcessConfig:
    data_path: str = os.path.join("artifacts", "preprocessed_data.csv")

class DataPreProcess:
    def __init__(self):
        self.pre_process_config = DataPreProcessConfig()

    def data_structuring(self, temp_path: Path) -> pd.DataFrame:
        '''
        Here basic structuring of the dataset will be performed like 
        Droping/Imputing of the data.
        '''
        logging.info("Entered the data processing zone.")

        df = pd.read_csv(temp_path)
        logging.info("Data Loaded successfully.")

        # Perform Data Cleaning
        # Check dataset size
        num_rows, num_cols = df.shape

        if num_rows > 2000:

            # Drop rows with missing values if dataset is large
            cleaned_dataframe = df.dropna(inplace=False)
            return cleaned_dataframe

        else:

            # Impute missing values if dataset is small
            try:
                for col in df.columns:
                    if df[col].isnull().sum() > 0:  # If column has missing values
                        if df[col].dtype == "object":
                            # For categorical columns, use mode (most frequent value)
                            df[col].fillna(df[col].mode()[0], inplace=True)
                        else:
                            # For numerical columns, determine whether to use mean or median
                            if df[col].skew() < 0.5:  # Low skewness (normal distribution)
                                df[col].fillna(df[col].mean(), inplace=True)  # Use mean
                            else:
                               df[col].fillna(df[col].median(), inplace=True)  # Use median
                cleaned_dataframe = df
                logging.info("Data cleaned successfully.")
                return cleaned_dataframe
            except Exception as e:
                logging.error(f"Error during data imputation: {e}")
                raise CustomException(e, sys)
            
    def label_encoding(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Here, label encoding will be performed in order to numerize the labels for Machine Learning models.
        '''
        # Perform Label Encoding
        try:
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])  # Convert to datetime
                df['year'] = df['date'].dt.year  # Extract year
                df['month'] = df['date'].dt.month  # Extract month
                df['day'] = df['date'].dt.day  # Extract day
                df.drop(columns=['date'], inplace=True)  # Drop original date column

            categorical_cols = df.select_dtypes(include=['object']).columns

            label_encoders = {}  # Store encoders for reference
            for col in categorical_cols:

                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])  # Encode categorical data
                label_encoders[col] = le  # Save the encoder for future use

            label_encoded_dataframe = df
            logging.info("Label Encoding completed successfully.")
            return label_encoded_dataframe

        except Exception as e:
            logging.error(f"Error during data cleaning: {e}")
            raise CustomException(e, sys)

    def onehot_encoder(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Here we will perform One Hot Encoding on the provided dataset.
        '''

        # Perform One Hot Encoding
        try:
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns

            if len(categorical_cols) == 0:
                print("No categorical columns found. No encoding needed.")
                encoded_dataframe = df

            encoder = OneHotEncoder(drop='first', sparse_output=False)  # drop='first' avoids dummy variable trap
            encoded_array = encoder.fit_transform(df[categorical_cols])

            encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out(categorical_cols))

            # Drop original categorical columns and concatenate encoded ones
            df = df.drop(columns=categorical_cols).reset_index(drop=True)
            encoded_df = encoded_df.reset_index(drop=True)

            onehot_encoded_dataframe = pd.concat([df, encoded_df], axis=1)
            logging.info("One Hot Encoding completed successfully.")
            return onehot_encoded_dataframe
        
        except Exception as e:
            logging.error(f"Error during data cleaning: {e}")
            raise CustomException(e, sys)

    def normalization(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Here we are going to apply normalization on our dataset.
        '''
        # Perform Normalization
        try:

            numerical_cols = df.select_dtypes(include=[np.number]).columns
            scaler = MinMaxScaler()
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
            normalized_dataframe = df
            logging.info("Normalization completed successfully.")
            return normalized_dataframe
        
        except Exception as e:
            logging.error(f"Error during data normalization: {e}")
            raise CustomException(e, sys)