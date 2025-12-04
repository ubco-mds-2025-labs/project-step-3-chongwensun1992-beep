from smartbudget.entity.constants import Limits


class RecordBase:
    """
    Base class for financial records such as Income and Expense.

    Provides:
    - Input validation and normalization
    - Property-based controlled access for `name` and `amount`
    - Serialization support via `to_dict`
    - Debug-friendly __repr__ output
    """

    def __init__(self, name: str, amount: float):
        self.name = name        # triggers setter + validation
        self.amount = amount    # triggers setter + validation

    # --------------------------------------------------------
    # Properties — safe attribute access
    # --------------------------------------------------------
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._validate_name(value)
        self._name = value.strip()

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float):
        self._validate_amount(value)
        self._amount = float(value)

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------
    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if len(name) > Limits.MAX_NAME_LEN:
            raise ValueError(
                f"Name cannot exceed {Limits.MAX_NAME_LEN} characters."
            )

    def _validate_amount(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be numeric.")
        # base record doesn't enforce positivity (Income/Expense override meaning)
        if amount == 0:
            raise ValueError("Amount cannot be zero.")

    # --------------------------------------------------------
    # Public Interface
    # --------------------------------------------------------
    def show(self) -> str:
        """One-line formatted display of the record."""
        return f"{self.name}: {self.amount:.2f}"

    def to_dict(self) -> dict:
        """Convert this record into a serializable dictionary."""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "amount": float(self.amount),
        }

    # --------------------------------------------------------
    # Debug & Utility
    # --------------------------------------------------------
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, amount={self.amount!r})"

    def __str__(self):
        return self.show()
