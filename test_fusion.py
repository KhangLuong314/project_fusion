"""
Testing & Robustness Suite for Project Fusion
by Khang Luong and Anthony Storm
CSCE 311 - Data Structure and Algorithm
"""

import unittest
import pandas as pd
import numpy as np
import os
from main import Execution

class TestFusionSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a small dummy dataset for testing
        cls.test_csv = 'test_fusion_data.csv'
        data = {
            'Magnetic Field Strength': [5.0, 6.0, 7.0, 8.0, 9.0],
            'Plasma Instabilities': [0.1, 0.2, 0.3, 0.4, 0.5],
            'Temperature': [15.0, 20.0, 25.0, 30.0, 35.0],
            'Fuel Density': [1.0, 1.1, 1.2, 1.3, 1.4],
            'Confinement Time': [0.5, 0.6, 0.7, 0.8, 0.9],
            'Neutron Yield': [1e15, 2e15, 3e15, 4e15, 5e15],
            'Power Output': [100, 200, 300, 400, 500],
            'Energy Input': [50, 50, 50, 50, 50],
            'Ignition': [0, 0, 1, 1, 1],
            'Magnetic Field Configuration': ['Tokamak', 'Stellarator', 'Tokamak', 'Stellarator', 'Tokamak']
        }
        pd.DataFrame(data).to_csv(cls.test_csv, index_label='ExperimentID')
        cls.executor = Execution(cls.test_csv)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_csv):
            os.remove(cls.test_csv)

    def test_data_cleaning_normal(self):
        """Test Case: Normal Data Cleaning and Efficiency Calculation."""
        self.assertIn('Overall Efficiency', self.executor.df.columns)
        # 100 / 50 = 2.0
        self.assertEqual(self.executor.df.iloc[0]['Overall Efficiency'], 2.0)

    def test_bst_range_search_normal(self):
        """Test Case: Normal BST Range Search."""
        results = self.executor.yield_bst.find_range(1.5e15, 4.5e15)
        # Should find IDs 1, 2, 3
        self.assertEqual(len(results), 3)
        self.assertIn(1, results)
        self.assertIn(2, results)
        self.assertIn(3, results)

    def test_bst_edge_case_empty_range(self):
        """Edge Case: Range search where no values exist."""
        results = self.executor.yield_bst.find_range(1e10, 2e10)
        self.assertEqual(len(results), 0)

    def test_bst_edge_case_single_point(self):
        """Edge Case: Range search that matches exactly one point."""
        results = self.executor.yield_bst.find_range(1e15, 1e15)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 0)

    def test_invalid_input_robustness(self):
        """Robustness: Check that specific stats handler doesn't crash on bad feature name."""
        # This shouldn't raise an exception because of our internal checks
        try:
            self.executor.view_specific_stats('Tokamak', 'mean', 'NonExistentFeature')
        except Exception as e:
            self.fail(f"view_specific_stats crashed on invalid feature: {e}")

    def test_unusual_input_extreme_values(self):
        """Extreme Case: Handling of extremely large numbers in Regression."""
        # Create a design matrix with one very large feature
        X = np.array([[1e20], [2e20]])
        y = np.array([[1], [2]])
        # The correlation_matrix function should handle this via numpy's linalg
        from toolbox import correlation_matrix
        coeffs = correlation_matrix(X, y)
        self.assertTrue(np.isfinite(coeffs).all())

if __name__ == '__main__':
    unittest.main()
