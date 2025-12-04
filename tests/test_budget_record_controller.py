import unittest
from unittest.mock import patch
from smartbudget.core_module_2.budget_record_controller import BudgetRecordController


class TestBudgetRecordController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[BudgetRecordController] setUpClass")

    def setUp(self):
        self.controller = BudgetRecordController()

    @patch("smartbudget.core_module_2.budget_record_controller.append_to_json")
    def test_add_income(self, mock_append):
        with patch("builtins.input", side_effect=["Salary", "3000", "Work"]):
            self.controller.add_income()

        self.assertEqual(len(self.controller.incomes), 1)
        inc = self.controller.incomes[0]
        self.assertEqual(inc.amount, 3000)
        self.assertEqual(inc.source, "work")
        self.assertEqual(inc.name, "Salary")
        mock_append.assert_called_once()

    @patch("smartbudget.core_module_2.budget_record_controller.append_to_json")
    def test_add_expense(self, mock_append):
        with patch("builtins.input", side_effect=["Taxi", "15", "Transport"]):
            self.controller.add_expense()

        self.assertEqual(len(self.controller.expenses), 1)
        exp = self.controller.expenses[0]
        self.assertEqual(exp.amount, 15)
        self.assertEqual(exp.category, "transport")
        self.assertEqual(exp.name, "Taxi")
        mock_append.assert_called_once()

    def tearDown(self):
        self.controller = None

    @classmethod
    def tearDownClass(cls):
        print("[BudgetRecordController] tearDownClass\n")



