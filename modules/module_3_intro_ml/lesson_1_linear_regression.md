# Lesson 1: Linear Regression

## Overview

Linear regression is one of the simplest and most widely used supervised learning algorithms. It models the linear relationship between input features and a continuous target variable.

## Key Concepts

### 1. What is Linear Regression?

Linear regression assumes a linear relationship:
```
y = mx + b + ε
```

Where:
- `y` = target variable (dependent variable)
- `x` = input feature (independent variable)
- `m` = slope (weight)
- `b` = intercept (bias)
- `ε` = error term

### 2. Cost Function (Loss Function)

Mean Squared Error (MSE):
```
MSE = (1/n) * Σ(y_actual - y_predicted)²
```

We aim to minimize this cost function.

### 3. Gradient Descent

An optimization algorithm that iteratively adjusts parameters to minimize the cost function:

```
θ = θ - α * (∂/∂θ) MSE
```

Where `α` is the learning rate.

### 4. Mathematical Intuition

In the case of multiple linear regression:
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

We can use the **Normal Equation** for closed-form solution:
```
β = (X^T X)^(-1) X^T y
```

## Assumptions

1. **Linearity**: Relationship between X and y is linear
2. **Independence**: Observations are independent
3. **Homoscedasticity**: Constant variance of errors
4. **Normality**: Errors are normally distributed
5. **No Multicollinearity**: Features are not highly correlated

## Implementation in Python

```python
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Sample data
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
y = np.array([2, 4, 5, 4, 5])

# Create and fit model
model = LinearRegression()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Get parameters
print(f"Slope: {model.coef_}")
print(f"Intercept: {model.intercept_}")

# Visualize
plt.scatter(X, y, color='blue', label='Actual')
plt.plot(X, y_pred, color='red', label='Predicted')
plt.legend()
plt.show()
```

## Evaluation Metrics

### 1. Mean Squared Error (MSE)
```python
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y, y_pred)
```

### 2. Root Mean Squared Error (RMSE)
```python
rmse = np.sqrt(mse)
```

### 3. Mean Absolute Error (MAE)
```python
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y, y_pred)
```

### 4. R² Score (Coefficient of Determination)
```python
from sklearn.metrics import r2_score
r2 = r2_score(y, y_pred)  # Range: 0 to 1 (higher is better)
```

## Advantages

✓ Simple and interpretable
✓ Computationally efficient
✓ Works well with small datasets
✓ Provides coefficient interpretability

## Disadvantages

✗ Assumes linear relationship
✗ Sensitive to outliers
✗ Cannot capture complex patterns
✗ Assumes constant variance

## Real-World Applications

- Stock price prediction
- Housing price estimation
- Sales forecasting
- Temperature prediction
- Risk assessment

## Key Takeaways

1. Linear regression is a fundamental algorithm for regression problems
2. It finds the best-fit line by minimizing error
3. Gradient descent is a popular optimization technique
4. Multiple evaluation metrics help assess model performance
5. Understanding assumptions is crucial for proper application

## Next Steps

- Practice with real datasets
- Learn about feature scaling and normalization
- Explore polynomial regression
- Study regularization techniques (Ridge, Lasso)
- Move to logistic regression for classification
