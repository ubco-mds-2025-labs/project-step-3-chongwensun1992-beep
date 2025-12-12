"""
Test suite for the insights module of SmartBudget.

This file validates record-splitting, type checking, JSON loading, and
detail-generation logic for income and expense objects. The tests isolate
core functionality by mocking file I/O and dependency behavior, ensuring
that insights functions operate correctly under both normal and exceptional
conditions. Visualization functions are also tested to confirm that plotting
logic executes without errors across different data scenarios.
"""

import os
import json
import shutil
import unittest
from unittest.mock import patch, MagicMock

from smartbudget.analysis_module_1.insights import (
    _validate_record_types,
    _split_records,
    _load_split,
    income_details,
    expense_details,
    plot_expense_by_category
)

from smartbudget.entity.income import Income

from smartbudget.entity.expense import Expense
from smartbudget.entity.base_record import RecordBase


TEST_DIR = "files"
TEST_FILE = "records.json"


class TestAnalysisModule(unittest.TestCase):

    def setUp(self):
        """Ensure a clean files directory."""
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        os.makedirs(TEST_DIR, exist_ok=True)

    def tearDown(self):
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    # ==================================================
    # Test _validate_record_types
    # ==================================================
    @patch("smartbudget.analysis_module_1.insights.logger.warning")
    def test_validate_record_types_warns_on_invalid(self, mock_warn):
        data = [Income("A", 100, "job"), RecordBase("X", 10)]
        _validate_record_types(data)
        mock_warn.assert_called_once()

    # ==================================================
    # Test _split_records
    # ==================================================
    def test_split_records_normal(self):
        records = [
            Income("A", 100, "job"),
            Expense("B", 20, "food")
        ]
        incomes, expenses = _split_records(records)
        self.assertEqual(len(incomes), 1)
        self.assertEqual(len(expenses), 1)

    def test_split_records_unknown(self):
        records = [
            RecordBase("X", 9),
            Income("A", 100, "work")
        ]
        incomes, expenses = _split_records(records)
        self.assertEqual(len(incomes), 1)
        self.assertEqual(len(expenses), 0)

    # ==================================================
    # Test _load_split success
    # ==================================================
    def test_load_split_success(self):
        sample = [
            {"type": "Income", "name": "A", "amount": 100, "source": "job"},
            {"type": "Expense", "name": "B", "amount": -20, "category": "food"}
        ]
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump(sample, f)

        incomes, expenses = _load_split()
        self.assertEqual(len(incomes), 1)
        self.assertEqual(len(expenses), 1)

    # ==================================================
    # Test _load_split exception branch
    # ==================================================
    @patch("smartbudget.analysis_module_1.insights.load_from_json", side_effect=Exception("boom"))
    def test_load_split_error(self, _mock):
        inc, exp = _load_split()
        self.assertEqual(inc, [])
        self.assertEqual(exp, [])

    # ==================================================
    # Test income_details()
    # ==================================================
    def test_income_details(self):
        sample = [
            {"type": "Income", "name": "A", "amount": 100, "source": "job"}
        ]
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump(sample, f)

        output = income_details()
        self.assertEqual(len(output), 1)
        self.assertIn("Income Record", output[0])

    @patch("smartbudget.analysis_module_1.insights.Income.describe", side_effect=Exception("fail"))
    def test_income_details_with_exception(self, _mock):
        sample = [
            {"type": "Income", "name": "A", "amount": 100, "source": "job"}
        ]
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump(sample, f)

        output = income_details()
        self.assertEqual(output, [])  # Should skip failed describe()

    # ==================================================
    # Test expense_details()
    # ==================================================
    def test_expense_details(self):
        sample = [
            {"type": "Expense", "name": "B", "amount": -20, "category": "food"}
        ]
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump(sample, f)

        output = expense_details()
        self.assertEqual(len(output), 1)
        self.assertIn("Expense Record", output[0])

    @patch("smartbudget.analysis_module_1.insights.Expense.describe", side_effect=Exception("fail"))
    def test_expense_details_with_exception(self, _mock):
        sample = [
            {"type": "Expense", "name": "B", "amount": -20, "category": "food"}
        ]
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump(sample, f)

        output = expense_details()
        self.assertEqual(output, [])

    # ==================================================
    # plot_expense_by_category()
    # ==================================================
    @patch("matplotlib.pyplot.show")
    def test_plot_expense_no_data(self, _mock_show):
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump([], f)
        plot_expense_by_category()  # No crash expected

    @patch("matplotlib.pyplot.show")
    def test_plot_expense_single_category(self, _mock_show):
        sample = [
            {"type": "Expense", "name": "B", "amount": -10, "category": "food"},
        ]
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump(sample, f)
        plot_expense_by_category()  # Single bar path

    @patch("matplotlib.pyplot.show")
    def test_plot_expense_multiple_categories(self, _mock_show):
        sample = [
            {"type": "Expense", "name": "B", "amount": -10, "category": "food"},
            {"type": "Expense", "name": "C", "amount": -20, "category": "travel"},
        ]
        with open(os.path.join(TEST_DIR, TEST_FILE), "w") as f:
            json.dump(sample, f)
        plot_expense_by_category()  # Multi-bar path


