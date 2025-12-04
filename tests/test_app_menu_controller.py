import unittest
from unittest.mock import patch, MagicMock
from smartbudget.core_module_2 import app_menu_controller
from smartbudget.entity.base_record import SmartBudgetError


class TestAppMenuController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[APP MENU] setUpClass")

    def setUp(self):
        # Replace real controllers with mocks
        self.mock_rec = MagicMock()
        self.mock_sys = MagicMock()

        app_menu_controller.rec = self.mock_rec
        app_menu_controller.sys = self.mock_sys

    # -----------------------------
    # 1. Add Income
    # -----------------------------
    @patch("builtins.input", side_effect=["1", "0"])
    @patch("builtins.print")
    def test_add_income(self, mock_print, mock_input):
        app_menu_controller.run()
        self.mock_rec.add_income.assert_called_once()

    # -----------------------------
    # 2. Add Expense
    # -----------------------------
    @patch("builtins.input", side_effect=["2", "0"])
    @patch("builtins.print")
    def test_add_expense(self, mock_print, mock_input):
        app_menu_controller.run()
        self.mock_rec.add_expense.assert_called_once()

    # -----------------------------
    # 3/4/5 Show functions
    # -----------------------------
    @patch("builtins.input", side_effect=["3", "4", "5", "0"])
    @patch("builtins.print")
    def test_show_functions(self, mock_print, mock_input):
        app_menu_controller.run()
        self.mock_rec.show_summary.assert_called_once()
        self.mock_rec.show_expense_details.assert_called_once()
        self.mock_rec.show_income_details.assert_called_once()

    # -----------------------------
    # 6/7/8/9 File operations
    # -----------------------------
    @patch("builtins.input", side_effect=["6", "7", "8", "9", "0"])
    @patch("builtins.print")
    def test_file_operations(self, mock_print, mock_input):
        app_menu_controller.run()
        self.mock_sys.save_data.assert_called_once()
        self.mock_sys.show_files.assert_called_once()
        self.mock_sys.delete_backup_file.assert_called_once()
        self.mock_sys.clear_data.assert_called_once()

    # -----------------------------
    # 10 Show chart
    # -----------------------------
    @patch("builtins.input", side_effect=["10", "0"])
    @patch("builtins.print")
    def test_show_chart(self, mock_print, mock_input):
        app_menu_controller.run()
        self.mock_rec.show_expense_plot.assert_called_once()

    # -----------------------------
    # Invalid choice
    # -----------------------------
    @patch("builtins.input", side_effect=["invalid", "0"])
    @patch("builtins.print")
    def test_invalid_choice(self, mock_print, mock_input):
        app_menu_controller.run()
        mock_print.assert_any_call("\n❌ Invalid choice. Try again.\n")

    # -----------------------------
    # Test SmartBudgetError in add_income
    # -----------------------------
    @patch("builtins.input", side_effect=["1", "0"])
    @patch("builtins.print")
    def test_add_income_error(self, mock_print, mock_input):
        self.mock_rec.add_income.side_effect = SmartBudgetError("test error")
        app_menu_controller.run()
        mock_print.assert_any_call("❌ Failed to add income: test error")

    # -----------------------------
    # Test generic Exception in add_expense
    # -----------------------------
    @patch("builtins.input", side_effect=["2", "0"])
    @patch("builtins.print")
    def test_add_expense_unexpected_error(self, mock_print, mock_input):
        self.mock_rec.add_expense.side_effect = Exception("boom")
        app_menu_controller.run()
        mock_print.assert_any_call("❌ Unexpected error: boom")

    # -----------------------------
    # KeyboardInterrupt exit
    # -----------------------------
    @patch("builtins.input", side_effect=KeyboardInterrupt)
    @patch("builtins.print")
    def test_keyboard_interrupt(self, mock_print, mock_input):
        app_menu_controller.run()
        mock_print.assert_any_call("\n\n⚠ Interrupted by user. Exiting safely...\n")

    # -----------------------------
    # Generic top-level unexpected exception
    # -----------------------------
    @patch("smartbudget.core_module_2.app_menu_controller.print_menu", side_effect=Exception("critical"))
    @patch("builtins.print")
    def test_top_level_critical_error(self, mock_print, mock_menu):
        app_menu_controller.run()
        mock_print.assert_any_call("\n❌ Critical error: critical\n")

    # -----------------------------
    # 0 → exit
    # -----------------------------
    @patch("builtins.input", side_effect=["0"])
    @patch("builtins.print")
    def test_exit(self, mock_print, mock_input):
        app_menu_controller.run()
        mock_print.assert_any_call("\nExiting SmartBudget. Goodbye!\n")

    @classmethod
    def tearDownClass(cls):
        print("[APP MENU] tearDownClass\n")
