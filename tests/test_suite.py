"""
Unified Test Suite Runner
-------------------------

This file collects all unittest test classes into one suite.
You can simply run:

    python test_suite.py

or from project root:

    python -m tests.test_suite
"""

import unittest
import sys
import os

# Ensure project root is in sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ============================
#  Import all test classes
# ============================

try:
    from tests.test_base_record import TestRecordBase
    from tests.test_income import TestIncome
    from tests.test_expense import TestExpense
    from tests.test_summary import TestSummary
    from tests.test_insights import TestInsights
    from tests.test_budget_record_controller import TestBudgetRecordController
    from tests.test_file_io_controller import TestFileIoDataController
    from tests.test_app_menu_controller import TestAppMenuController
except Exception:
    # fallback when running inside tests/ directly
    from test_base_record import TestRecordBase
    from test_income import TestIncome
    from test_expense import TestExpense
    from test_summary import TestSummary
    from test_insights import TestInsights
    from test_budget_record_controller import TestBudgetRecordController
    from test_file_io_controller import TestFileIoDataController
    from test_app_menu_controller import TestAppMenuController


# ============================
#  Build the test suite
# ============================

def suite():
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(loader.loadTestsFromTestCase(TestRecordBase))
    test_suite.addTests(loader.loadTestsFromTestCase(TestIncome))
    test_suite.addTests(loader.loadTestsFromTestCase(TestExpense))
    test_suite.addTests(loader.loadTestsFromTestCase(TestSummary))
    test_suite.addTests(loader.loadTestsFromTestCase(TestInsights))
    test_suite.addTests(loader.loadTestsFromTestCase(TestBudgetRecordController))
    test_suite.addTests(loader.loadTestsFromTestCase(TestFileIoDataController))
    test_suite.addTests(loader.loadTestsFromTestCase(TestAppMenuController))

    return test_suite


# ============================
#  Main execution
# ============================
if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    print("\n=== Running SmartBudget Full Test Suite ===\n")
    runner.run(suite())
