import unittest

# ===== Import all test classes =====
from test_base_record import TestRecordBase
from test_income_expense import TestIncomeExpense
from test_summary import TestSummary
from test_insights import TestInsights
from test_budget_record_controller import TestBudgetRecordController
from test_file_io_controller import TestFileIoDataController


def suite():
    loader = unittest.TestLoader()
    s = unittest.TestSuite()

    # Add each test class explicitly
    s.addTests(loader.loadTestsFromTestCase(TestRecordBase))
    s.addTests(loader.loadTestsFromTestCase(TestIncomeExpense))
    s.addTests(loader.loadTestsFromTestCase(TestSummary))
    s.addTests(loader.loadTestsFromTestCase(TestInsights))
    s.addTests(loader.loadTestsFromTestCase(TestBudgetRecordController))
    s.addTests(loader.loadTestsFromTestCase(TestFileIoDataController))

    return s


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
