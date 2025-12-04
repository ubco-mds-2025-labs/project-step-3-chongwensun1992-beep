import unittest
from unittest.mock import patch, MagicMock
from smartbudget.core_module_2.budget_record_controller import BudgetRecordController
from smartbudget.entity.base_record import SmartBudgetError


class TestBudgetRecordController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[BUDGET CTRL] setUpClass")

    def setUp(self):
        self.ctrl = BudgetRecordController()

    # --------------------------------------------------------
    # show_summary (normal path)
    # --------------------------------------------------------
    @patch("builtins.print")
    @patch("smartbudget.analysis_module_1.summary.total_income", return_value=500)
    @patch("smartbudget.analysis_module_1.summary.total_expenses", return_value=200)
    @patch("smartbudget.analysis_module_1.summary.budget_balance", return_value=300)
    def test_show_summary(self, *_):
        self.ctrl.show_summary()

    # --------------------------------------------------------
    # show_summary (exception path)
    # --------------------------------------------------------
    @patch("smartbudget.analysis_module_1.summary.total_income", side_effect=Exception("boom"))
    def test_show_summary_error(self, *_):
        with self.assertRaises(SmartBudgetError):
            self.ctrl.show_summary()

    # --------------------------------------------------------
    # show_income_details normal + empty path
    # --------------------------------------------------------
    @patch("builtins.print")
    @patch("smartbudget.analysis_module_1.insights.income_details", return_value=[])
    def test_show_income_details_empty(self, *_):
        self.ctrl.show_income_details()

    @patch("builtins.print")
    @patch("smartbudget.analysis_module_1.insights.income_details", return_value=["A", "B"])
    def test_show_income_details_nonempty(self, mock_details, mock_print):
        self.ctrl.show_income_details()
        mock_details.assert_called_once()

    # exception path
    @patch("smartbudget.analysis_module_1.insights.income_details", side_effect=Exception("fail"))
    def test_show_income_details_error(self, *_):
        with self.assertRaises(SmartBudgetError):
            self.ctrl.show_income_details()

    # --------------------------------------------------------
    # show_expense_details normal + empty path
    # --------------------------------------------------------
    @patch("builtins.print")
    @patch("smartbudget.analysis_module_1.insights.expense_details", return_value=[])
    def test_show_expense_details_empty(self, *_):
        self.ctrl.show_expense_details()

    @patch("builtins.print")
    @patch("smartbudget.analysis_module_1.insights.expense_details", return_value=["A"])
    def test_show_expense_details_nonempty(self, *_):
        self.ctrl.show_expense_details()

    @patch("smartbudget.analysis_module_1.insights.expense_details", side_effect=Exception("boom"))
    def test_show_expense_details_error(self, *_):
        with self.assertRaises(SmartBudgetError):
            self.ctrl.show_expense_details()

    # --------------------------------------------------------
    # show_expense_plot normal + exception
    # --------------------------------------------------------
    @patch("builtins.print")
    @patch("smartbudget.analysis_module_1.insights.plot_expense_by_category")
    def test_show_expense_plot(self, mock_plot, *_):
        self.ctrl.show_expense_plot()
        mock_plot.assert_called_once()

    @patch("smartbudget.analysis_module_1.insights.plot_expense_by_category", side_effect=Exception("fail"))
    def test_show_expense_plot_error(self, *_):
        with self.assertRaises(SmartBudgetError):
            self.ctrl.show_expense_plot()

    # --------------------------------------------------------
    # add_income normal
    # --------------------------------------------------------
    @patch("smartbudget.file_io_module_3.append_to_json")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Gift", "100", "Friend"])
    def test_add_income(self, *_):
        self.ctrl.add_income()
        self.assertEqual(len(self.ctrl.incomes), 1)
        inc = self.ctrl.incomes[0]
        self.assertEqual(inc.name, "Gift")
        self.assertEqual(inc.amount, 100)
        self.assertEqual(inc.source, "friend")

    # add_income invalid amount (ValueError → SmartBudgetError branch)
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["IncomeX", "abc"])  # amount invalid
    def test_add_income_invalid_amount(self, *_):
        self.ctrl.add_income()  # does NOT crash

    # append_to_json failure path
    @patch("smartbudget.file_io_module_3.append_to_json", side_effect=Exception("fail"))
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Gift", "100", "Friend"])
    def test_add_income_save_error(self, *_):
        self.ctrl.add_income()  # should catch SmartBudgetError internally

    # --------------------------------------------------------
    # add_expense normal
    # --------------------------------------------------------
    @patch("smartbudget.file_io_module_3.append_to_json")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Taxi", "30", "Transport"])
    def test_add_expense(self, *_):
        self.ctrl.add_expense()
        self.assertEqual(len(self.ctrl.expenses), 1)
        exp = self.ctrl.expenses[0]
        self.assertEqual(exp.amount, 30)
        self.assertEqual(exp.category, "transport")

    # invalid amount
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Taxi", "abc"])
    def test_add_expense_invalid_amount(self, *_):
        self.ctrl.add_expense()

    # append_to_json failure
    @patch("smartbudget.file_io_module_3.append_to_json", side_effect=Exception("fail"))
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Taxi", "30", "Transport"])
    def test_add_expense_save_error(self, *_):
        self.ctrl.add_expense()

    # unexpected exception inside Income()/Expense()
    @patch("smartbudget.entity.income.Income.__init__", side_effect=Exception("boom"))
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Gift", "100", "Friend"])
    def test_add_income_unexpected(self, *_):
        self.ctrl.add_income()  # does not crash

    @patch("smartbudget.entity.expense.Expense.__init__", side_effect=Exception("boom"))
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Taxi", "30", "Transport"])
    def test_add_expense_unexpected(self, *_):
        self.ctrl.add_expense()

    def tearDown(self):
        self.ctrl = None

    @classmethod
    def tearDownClass(cls):
        print("[BUDGET CTRL] tearDownClass\n")
