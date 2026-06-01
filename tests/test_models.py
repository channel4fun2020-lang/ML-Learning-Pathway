"""Unit tests for ML models"""

import pytest
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error


class TestLinearRegression:
    """Test linear regression model"""
    
    def setup_method(self):
        """Setup test data"""
        self.X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
        self.y = np.array([2, 4, 5, 4, 5])
    
    def test_model_training(self):
        """Test model training"""
        model = LinearRegression()
        model.fit(self.X, self.y)
        
        assert model.coef_ is not None
        assert model.intercept_ is not None
    
    def test_predictions(self):
        """Test model predictions"""
        model = LinearRegression()
        model.fit(self.X, self.y)
        
        predictions = model.predict(self.X)
        
        assert predictions.shape == self.y.shape
        assert not np.any(np.isnan(predictions))
    
    def test_mse_score(self):
        """Test MSE calculation"""
        model = LinearRegression()
        model.fit(self.X, self.y)
        
        predictions = model.predict(self.X)
        mse = mean_squared_error(self.y, predictions)
        
        assert mse >= 0
        assert mse < 10  # Reasonable threshold


class TestDataProcessing:
    """Test data processing utilities"""
    
    def test_train_test_split(self):
        """Test train-test split"""
        X, y = load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        assert len(X_train) + len(X_test) == len(X)
        assert len(y_train) + len(y_test) == len(y)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
