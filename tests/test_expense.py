import unittest
from unittest.mock import patch, PropertyMock
from smartbudget.entity.expense import Expense
from smartbudget.entity.base_record import SmartBudgetError


class TestExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[TestExpense] setUpClass")

    def setUp(self):
        self.exp = Expense("Taxi", 15, "Transport")

    # --------------------------------------------------------
    # Valid cases
    # --------------------------------------------------------
    def test_valid_expense(self):
        self.assertEqual(self.exp.name, "Taxi")
        self.assertEqual(self.exp.amount, 15)
        self.assertEqual(self.exp.category, "transport")
        self.assertIn("Expense Record", self.exp.describe())

    def test_to_dict_valid(self):
        d = self.exp.to_dict()
        self.assertEqual(d["type"], "Expense")
        self.assertEqual(d["amount"], 15.0)
        self.assertEqual(d["category"], "transport")
        self.assertIsInstance(d, dict)

    # --------------------------------------------------------
    # __init__ invalid input branches
    # --------------------------------------------------------
    def test_invalid_init(self):
        with self.assertRaises(SmartBudgetError):
            Expense("", 10, "Food")

        with self.assertRaises(SmartBudgetError):
            Expense("Food", -1, "Cat")

        with self.assertRaises(SmartBudgetError):
            Expense("Food", 1, "")

        with self.assertRaises(SmartBudgetError):
            Expense("Food", "abc", "Cat")

    # 模拟 base class 触发 SmartBudgetError
    @patch("smartbudget.entity.expense.RecordBase.__init__", side_effect=Exception("boom"))
    def test_base_class_failure(self, mock_base):
        with self.assertRaises(SmartBudgetError):
            Expense("Food", 10, "Cat")

    # --------------------------------------------------------
    # category.setter invalid branches
    # --------------------------------------------------------
    def test_category_setter_invalid(self):
        with self.assertRaises(SmartBudgetError):
            self.exp.category = 123

        with self.assertRaises(SmartBudgetError):
            self.exp.category = ""

    # --------------------------------------------------------
    # describe() error branch
    # --------------------------------------------------------
    @patch("smartbudget.entity.expense.Expense.name", new_callable=PropertyMock)
    def test_describe_exception(self, mock_name):
        mock_name.side_effect = Exception("desc error")

        with self.assertRaises(SmartBudgetError):
            self.exp.describe()

    # --------------------------------------------------------
    # to_dict() error branch
    # --------------------------------------------------------
    @patch("smartbudget.entity.expense.Expense.amount", new_callable=PropertyMock)
    def test_to_dict_exception(self, mock_amt):
        mock_amt.side_effect = Exception("dict error")

        with self.assertRaises(SmartBudgetError):
            self.exp.to_dict()

    def tearDown(self):
        self.exp = None

    @classmethod
    def tearDownClass(cls):
        print("[TestExpense] tearDownClass\n")
