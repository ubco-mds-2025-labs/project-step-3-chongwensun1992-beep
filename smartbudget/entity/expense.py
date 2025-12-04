from .base_record import RecordBase


class Expense(RecordBase):
    """
    Represents a single expense record.

    This class stores the expense name, amount (always positive),
    and category. It includes input validation, normalization, and
    controlled attribute access through properties.
    """

    def __init__(self, name: str, amount: float, category: str):
        # ---- Validation ----
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Expense name must be a non-empty string.")

        if not isinstance(amount, (int, float)):
            raise TypeError("Expense amount must be numeric.")

        if amount <= 0:
            raise ValueError("Expense amount must be positive.")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Expense category must be a non-empty string.")

        # Call base class
        super().__init__(name.strip(), float(abs(amount)))

        # ---- Normalization ----
        self._category = category.strip().lower()

    # --------------------------------------------------------
    # Properties (safe attribute access)
    # --------------------------------------------------------
    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string.")
        self._category = value.strip().lower()

    # --------------------------------------------------------
    # description
    # --------------------------------------------------------
    def describe(self) -> str:
        return (
            "Expense Record\n"
            f"  Name     : {self.name}\n"
            f"  Category : {self.category}\n"
            f"  Amount   : {self.amount:.2f}\n"
        )

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "type": "Expense",
            "name": self.name,
            "amount": float(self.amount),
            "category": self.category,
        }
