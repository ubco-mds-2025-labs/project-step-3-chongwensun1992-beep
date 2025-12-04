import unittest
from unittest.mock import patch, PropertyMock
from smartbudget.entity.base_record import RecordBase, SmartBudgetError
from smartbudget.entity.constants import Limits


class TestRecordBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[TestRecordBase] setUpClass")

    def setUp(self):
        self.record = RecordBase("Sample", 20)

    # -------------------------------------------------------
    # Valid record tests
    # -------------------------------------------------------
    def test_valid_record(self):
        self.assertEqual(self.record.name, "Sample")
        self.assertEqual(self.record.amount, 20)
        self.assertIsInstance(self.record.name, str)
        self.assertGreater(self.record.amount, 0)

    def test_to_dict_valid(self):
        d = self.record.to_dict()
        self.assertEqual(d["type"], "RecordBase")
        self.assertEqual(d["name"], "Sample")
        self.assertEqual(d["amount"], 20.0)

    def test_repr_str(self):
        self.assertIn("RecordBase", repr(self.record))
        self.assertEqual(str(self.record), "Sample: 20.00")

    # -------------------------------------------------------
    # Initialization failures
    # -------------------------------------------------------
    def test_invalid_initialization(self):
        with self.assertRaises(SmartBudgetError):
            RecordBase("", 10)

        with self.assertRaises(SmartBudgetError):
            RecordBase(123, 10)

        with self.assertRaises(SmartBudgetError):
            RecordBase("Test", "abc")

        with self.assertRaises(SmartBudgetError):
            RecordBase("Test", 0)

    # -------------------------------------------------------
    # name setter invalid cases
    # -------------------------------------------------------
    def test_name_setter_invalid(self):
        with self.assertRaises(SmartBudgetError):
            self.record.name = 123

        with self.assertRaises(SmartBudgetError):
            self.record.name = ""

        long_name = "A" * (Limits.MAX_NAME_LEN + 1)
        with self.assertRaises(SmartBudgetError):
            self.record.name = long_name

    # -------------------------------------------------------
    # amount setter invalid cases
    # -------------------------------------------------------
    def test_amount_setter_invalid(self):
        with self.assertRaises(SmartBudgetError):
            self.record.amount = "abc"

        with self.assertRaises(SmartBudgetError):
            self.record.amount = 0

    # -------------------------------------------------------
    # show() error handling
    # -------------------------------------------------------
    @patch("smartbudget.entity.base_record.RecordBase.name", new_callable=PropertyMock)
    def test_show_exception(self, mock_name_prop):
        mock_name_prop.side_effect = Exception("boom")

        with self.assertRaises(SmartBudgetError):
            self.record.show()

    # -------------------------------------------------------
    # to_dict() error handling
    # -------------------------------------------------------
    @patch("smartbudget.entity.base_record.RecordBase.amount", new_callable=PropertyMock)
    def test_to_dict_exception(self, mock_amt_prop):
        mock_amt_prop.side_effect = Exception("boom")

        with self.assertRaises(SmartBudgetError):
            self.record.to_dict()

    def tearDown(self):
        self.record = None

    @classmethod
    def tearDownClass(cls):
        print("[TestRecordBase] tearDownClass\n")
