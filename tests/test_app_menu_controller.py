import unittest
from unittest.mock import patch
import smartbudget.core_module_2.app_menu_controller as app_menu


class TestAppMenuController(unittest.TestCase):

    @patch("builtins.input", side_effect=["0"])
    def test_exit(self, mock_input):
        """Test that entering 0 exits without crashing."""
        # run() should exit cleanly
        app_menu.run()

        # 只验证 input 被调用、程序未崩溃
        mock_input.assert_called_once()


    @patch("builtins.input", side_effect=["1", "0"])
    @patch("smartbudget.core_module_2.budget_record_controller.BudgetRecordController.add_income")
    def test_add_income(self, mock_add_income, mock_input):
        app_menu.run()
        mock_add_income.assert_called_once()


    @patch("builtins.input", side_effect=["2", "0"])
    @patch("smartbudget.core_module_2.budget_record_controller.BudgetRecordController.add_expense")
    def test_add_expense(self, mock_add_expense, mock_input):
        app_menu.run()
        mock_add_expense.assert_called_once()


    @patch("builtins.input", side_effect=["3", "0"])
    @patch("smartbudget.core_module_2.budget_record_controller.BudgetRecordController.show_summary")
    def test_show_summary(self, mock_show_summary, mock_input):
        app_menu.run()
        mock_show_summary.assert_called_once()


    @patch("builtins.input", side_effect=["4", "0"])
    @patch("smartbudget.core_module_2.budget_record_controller.BudgetRecordController.show_expense_details")
    def test_show_expense_details(self, mock_show_details, mock_input):
        app_menu.run()
        mock_show_details.assert_called_once()


    @patch("builtins.input", side_effect=["5", "0"])
    @patch("smartbudget.core_module_2.budget_record_controller.BudgetRecordController.show_income_details")
    def test_show_income_details(self, mock_show_details, mock_input):
        app_menu.run()
        mock_show_details.assert_called_once()


    @patch("builtins.input", side_effect=["10", "0"])
    @patch("smartbudget.core_module_2.budget_record_controller.BudgetRecordController.show_expense_plot")
    def test_show_expense_plot(self, mock_show_plot, mock_input):
        app_menu.run()
        mock_show_plot.assert_called_once()


    @patch("builtins.input", side_effect=["99", "0"])
    @patch("builtins.print")  # 用 print 替代 sys.stdout.write
    def test_invalid_choice(self, mock_print, mock_input):
        """Should print invalid choice but not crash."""
        app_menu.run()

        printed_text = "".join(str(call.args[0]) for call in mock_print.call_args_list)
        self.assertIn("Invalid choice", printed_text)



