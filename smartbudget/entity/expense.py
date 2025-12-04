from .base_record import RecordBase, SmartBudgetError


class Expense(RecordBase):
    """
    Simple Expense class compatible with unittest patching.
    """

    def __init__(self, name: str, amount: float, category: str):
        # Let RecordBase validate name + amount without extra wrapping
        super().__init__(name, amount)

        if not isinstance(category, str) or not category.strip():
            raise SmartBudgetError("Category must be a non-empty string")

        self._category = category.strip().lower()

    # --------------------------------------------------------
    # category property
    # --------------------------------------------------------
    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise SmartBudgetError("Category must be a non-empty string")
        self._category = value.strip().lower()

    # --------------------------------------------------------
    # describe() — catch exceptions only once
    # --------------------------------------------------------
    def describe(self) -> str:
        try:
            return (
                "Expense Record\n"
                f"  Name     : {self.name}\n"
                f"  Category : {self.category}\n"
                f"  Amount   : {self.amount:.2f}\n"
            )
        except Exception as e:
            raise SmartBudgetError(f"Failed to describe expense: {e}")

    # --------------------------------------------------------
    # to_dict() — catch exceptions only once
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        try:
            return {
                "type": "Expense",
                "name": self.name,
                "amount": float(self.amount),
                "category": self.category,
            }
        except Exception as e:
            raise SmartBudgetError(f"Failed to_dict Expense: {e}")
