import unittest
from unittest.mock import patch, PropertyMock
from smartbudget.entity.income import Income
from smartbudget.entity.base_record import SmartBudgetError


class TestIncome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[TestIncome] setUpClass")

    def setUp(self):
        self.inc = Income("Gift", 100, "Friend")

    # --------------------------------------------------------
    # Valid branches
    # --------------------------------------------------------
    def test_valid_income(self):
        self.assertEqual(self.inc.name, "Gift")
        self.assertEqual(self.inc.amount, 100)
        self.assertEqual(self.inc.source, "friend")
        self.assertIn("Income Record", self.inc.describe())

    def test_to_dict_valid(self):
        d = self.inc.to_dict()
        self.assertEqual(d["type"], "Income")
        self.assertEqual(d["name"], "Gift")
        self.assertEqual(d["amount"], 100.0)
        self.assertEqual(d["source"], "friend")

    # --------------------------------------------------------
    # __init__ error branches
    # --------------------------------------------------------
    def test_invalid_init(self):
        # invalid name
        with self.assertRaises(SmartBudgetError):
            Income("", 100, "Work")

        with self.assertRaises(SmartBudgetError):
            Income(123, 100, "Work")

        # invalid amount
        with self.assertRaises(SmartBudgetError):
            Income("Test", "abc", "Work")

        with self.assertRaises(SmartBudgetError):
            Income("Test", -5, "Work")

        # invalid source
        with self.assertRaises(SmartBudgetError):
            Income("Test", 10, "")

        with self.assertRaises(SmartBudgetError):
            Income("Test", 10, 123)

    # base class __init__ exception
    @patch("smartbudget.entity.income.RecordBase.__init__", side_effect=Exception("boom"))
    def test_base_init_failure(self, mock_base):
        with self.assertRaises(SmartBudgetError):
            Income("Test", 10, "Work")

    # --------------------------------------------------------
    # source.setter exceptions
    # --------------------------------------------------------
    def test_invalid_source_setter(self):
        with self.assertRaises(SmartBudgetError):
            self.inc.source = 123
        with self.assertRaises(SmartBudgetError):
            self.inc.source = ""

    # --------------------------------------------------------
    # describe() error branch
    # --------------------------------------------------------
    @patch("smartbudget.entity.income.Income.name", new_callable=PropertyMock)
    def test_describe_error(self, mock_name):
        mock_name.side_effect = Exception("desc error")

        with self.assertRaises(SmartBudgetError):
            self.inc.describe()

    # --------------------------------------------------------
    # to_dict() error branch
    # --------------------------------------------------------
    @patch("smartbudget.entity.income.Income.source", new_callable=PropertyMock)
    def test_to_dict_error(self, mock_source):
        mock_source.side_effect = Exception("dict error")

        with self.assertRaises(SmartBudgetError):
            self.inc.to_dict()

    def tearDown(self):
        self.inc = None

    @classmethod
    def tearDownClass(cls):
        print("[TestIncome] tearDownClass\n")
