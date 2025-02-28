"""
Unit tests for utility functions in src/utils.py
"""

import unittest
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import (
    load_data, preprocess_data, extract_ticker_data, 
    calculate_daily_returns, calculate_rolling_statistics,
    calculate_volatility, calculate_sharpe_ratio, calculate_var
)

class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data"""
        # Create a sample DataFrame that mimics the structure of our financial data
        dates = pd.date_range(start='2020-01-01', end='2020-01-10')
        
        # Sample data for TSLA
        tsla_data = {
            'TSLA_Open': np.linspace(100, 110, len(dates)),
            'TSLA_High': np.linspace(105, 115, len(dates)),
            'TSLA_Low': np.linspace(95, 105, len(dates)),
            'TSLA_Close': np.linspace(102, 112, len(dates)),
            'TSLA_Adj Close': np.linspace(102, 112, len(dates)),
            'TSLA_Volume': np.random.randint(1000000, 5000000, size=len(dates))
        }
        
        # Sample data for SPY
        spy_data = {
            'SPY_Open': np.linspace(300, 310, len(dates)),
            'SPY_High': np.linspace(305, 315, len(dates)),
            'SPY_Low': np.linspace(295, 305, len(dates)),
            'SPY_Close': np.linspace(302, 312, len(dates)),
            'SPY_Adj Close': np.linspace(302, 312, len(dates)),
            'SPY_Volume': np.random.randint(10000000, 50000000, size=len(dates))
        }
        
        # Combine the data
        cls.test_data = pd.DataFrame({**tsla_data, **spy_data}, index=dates)
        
        # Add some missing values for testing preprocessing
        cls.test_data_with_na = cls.test_data.copy()
        cls.test_data_with_na.loc[cls.test_data_with_na.index[2], 'TSLA_Close'] = np.nan
        cls.test_data_with_na.loc[cls.test_data_with_na.index[3], 'SPY_Volume'] = np.nan
        
        # Save test data to a temporary CSV file
        os.makedirs('tests/temp', exist_ok=True)
        cls.test_data.to_csv('tests/temp/test_data.csv')
        cls.test_data_with_na.to_csv('tests/temp/test_data_with_na.csv')
    
    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files"""
        if os.path.exists('tests/temp/test_data.csv'):
            os.remove('tests/temp/test_data.csv')
        if os.path.exists('tests/temp/test_data_with_na.csv'):
            os.remove('tests/temp/test_data_with_na.csv')
        if os.path.exists('tests/temp'):
            os.rmdir('tests/temp')
    
    def test_extract_ticker_data(self):
        """Test extract_ticker_data function"""
        # Extract TSLA data
        tsla_data = extract_ticker_data(self.test_data, 'TSLA')
        
        # Check dimensions
        self.assertEqual(len(tsla_data.columns), 6)
        self.assertEqual(len(tsla_data), len(self.test_data))
        
        # Check column names are properly renamed
        self.assertTrue('Open' in tsla_data.columns)
        self.assertTrue('Close' in tsla_data.columns)
        self.assertTrue('Volume' in tsla_data.columns)
        
        # Test with specific columns
        tsla_price = extract_ticker_data(self.test_data, 'TSLA', columns=['Close', 'Volume'])
        self.assertEqual(len(tsla_price.columns), 2)
        self.assertTrue('Close' in tsla_price.columns)
        self.assertTrue('Volume' in tsla_price.columns)
    
    def test_preprocess_data(self):
        """Test preprocess_data function"""
        # Check that missing values are handled
        processed_data = preprocess_data(self.test_data_with_na)
        
        # Verify no missing values remain
        self.assertEqual(processed_data.isnull().sum().sum(), 0)
        
        # Verify dimensions are preserved
        self.assertEqual(processed_data.shape, self.test_data_with_na.shape)
    
    def test_calculate_daily_returns(self):
        """Test calculate_daily_returns function"""
        tsla_data = extract_ticker_data(self.test_data, 'TSLA')
        returns = calculate_daily_returns(tsla_data)
        
        # Check returns calculation
        self.assertEqual(len(returns), len(self.test_data) - 1)  # One less due to pct_change
        
        # Manually calculate first return to verify
        expected_first_return = (tsla_data['Adj Close'][1] / tsla_data['Adj Close'][0] - 1) * 100
        self.assertAlmostEqual(returns.iloc[0], expected_first_return)
    
    def test_calculate_rolling_statistics(self):
        """Test calculate_rolling_statistics function"""
        tsla_data = extract_ticker_data(self.test_data, 'TSLA')
        
        # Test with window size of 3
        rolling_mean, rolling_std = calculate_rolling_statistics(tsla_data, window=3)
        
        # Check lengths
        self.assertEqual(len(rolling_mean), len(tsla_data))
        self.assertEqual(len(rolling_std), len(tsla_data))
        
        # First 2 values should be NaN (window size - 1)
        self.assertTrue(np.isnan(rolling_mean.iloc[0]))
        self.assertTrue(np.isnan(rolling_mean.iloc[1]))
        self.assertFalse(np.isnan(rolling_mean.iloc[2]))
    
    def test_calculate_volatility(self):
        """Test calculate_volatility function"""
        tsla_data = extract_ticker_data(self.test_data, 'TSLA')
        returns = calculate_daily_returns(tsla_data)
        
        # Test with window size of 3
        volatility = calculate_volatility(returns, window=3)
        
        # Check length
        self.assertEqual(len(volatility), len(returns))
        
        # First 2 values should be NaN (window size - 1)
        self.assertTrue(np.isnan(volatility.iloc[0]))
        self.assertTrue(np.isnan(volatility.iloc[1]))
        self.assertFalse(np.isnan(volatility.iloc[2]))
    
    def test_calculate_sharpe_ratio(self):
        """Test calculate_sharpe_ratio function"""
        tsla_data = extract_ticker_data(self.test_data, 'TSLA')
        returns = calculate_daily_returns(tsla_data)
        
        # Calculate Sharpe ratio
        sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.01)
        
        # Check it's a float
        self.assertIsInstance(sharpe, float)
    
    def test_calculate_var(self):
        """Test calculate_var function"""
        tsla_data = extract_ticker_data(self.test_data, 'TSLA')
        returns = calculate_daily_returns(tsla_data)
        
        # Calculate VaR at 95% confidence
        var = calculate_var(returns, confidence_level=0.95)
        
        # Check it's a float
        self.assertIsInstance(var, float)
        
        # VaR should be negative or zero for normal return distributions
        self.assertLessEqual(var, 0)

if __name__ == '__main__':
    unittest.main()