import unittest
import logging
from smartbudget.entity.income import Income
from smartbudget.entity.expense import Expense

logger = logging.getLogger(__name__)


class TestIncomeExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("=== [TestIncomeExpense] Preparing test-level constants ===")
        cls.sample_income = Income("Salary", 3000, "Work")
        cls.sample_expense = Expense("Food", 20, "Groceries")

    def setUp(self):
        logger.debug("[TestIncomeExpense] setUp: initializing fresh test objects")
        self.income = Income("Gift", 100, "Friend")
        self.expense = Expense("Taxi", 15, "Transport")

    def test_income(self):
        logger.debug("[TestIncomeExpense] Running test_income")
        self.assertEqual(self.income.amount, 100)

        # ⬇⬇⬇ FIXED: source is automatically lowercased
        self.assertEqual(self.income.source, "friend")

        self.assertTrue(self.income.amount > 0)
        self.assertEqual(self.income.to_dict()["type"], "Income")

    def test_expense(self):
        logger.debug("[TestIncomeExpense] Running test_expense")
        self.assertEqual(self.expense.amount, 15)

        # ⬇⬇⬇ FIXED: category is automatically lowercased
        self.assertEqual(self.expense.category, "transport")

        self.assertGreater(self.expense.amount, 0)
        self.assertEqual(self.expense.to_dict()["type"], "Expense")

    def tearDown(self):
        logger.debug("[TestIncomeExpense] tearDown: nullifying objects")
        self.income = None
        self.expense = None

    @classmethod
    def tearDownClass(cls):
        logger.info("=== [TestIncomeExpense] Class-level cleanup complete ===")
