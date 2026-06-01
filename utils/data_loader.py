"""Utility functions for loading and processing datasets"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import os


class DataLoader:
    """Load and preprocess datasets"""
    
    @staticmethod
    def load_csv(filepath, **kwargs):
        """
        Load CSV file
        
        Args:
            filepath (str): Path to CSV file
            **kwargs: Additional arguments for pd.read_csv
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            return pd.read_csv(filepath, **kwargs)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filepath} not found")
        except Exception as e:
            raise Exception(f"Error loading file: {str(e)}")
    
    @staticmethod
    def load_dataset(name):
        """
        Load built-in datasets
        
        Args:
            name (str): Dataset name
            
        Returns:
            pd.DataFrame: Dataset
        """
        datasets = {
            'iris': 'datasets/iris.csv',
            'titanic': 'datasets/titanic.csv',
            'housing': 'datasets/housing.csv',
            'digits': 'datasets/digits.csv'
        }
        
        if name not in datasets:
            raise ValueError(f"Dataset {name} not found")
        
        return DataLoader.load_csv(datasets[name])
    
    @staticmethod
    def split_data(X, y, test_size=0.2, random_state=42):
        """
        Split data into train and test sets
        
        Args:
            X (array-like): Features
            y (array-like): Target
            test_size (float): Test set size
            random_state (int): Random seed
            
        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    @staticmethod
    def scale_data(X_train, X_test, method='standard'):
        """
        Scale features
        
        Args:
            X_train (array-like): Training features
            X_test (array-like): Testing features
            method (str): 'standard' or 'minmax'
            
        Returns:
            tuple: Scaled X_train, X_test
        """
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled
    
    @staticmethod
    def handle_missing_values(df, method='mean'):
        """
        Handle missing values
        
        Args:
            df (pd.DataFrame): Input dataframe
            method (str): 'mean', 'median', 'drop', 'forward_fill'
            
        Returns:
            pd.DataFrame: Dataframe with missing values handled
        """
        if method == 'mean':
            return df.fillna(df.mean())
        elif method == 'median':
            return df.fillna(df.median())
        elif method == 'drop':
            return df.dropna()
        elif method == 'forward_fill':
            return df.fillna(method='ffill')
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def get_data_info(df):
        """
        Get information about dataset
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            dict: Dataset information
        """
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'statistics': df.describe().to_dict()
        }
