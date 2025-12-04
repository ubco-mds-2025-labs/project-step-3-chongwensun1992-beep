from .base_record import RecordBase, SmartBudgetError


class Income(RecordBase):
    """
    Simple Income class compatible with unittest patching.
    """

    def __init__(self, name: str, amount: float, source: str):
        # Let RecordBase validate name & amount
        super().__init__(name, amount)

        if not isinstance(source, str) or not source.strip():
            raise SmartBudgetError("Source must be a non-empty string")

        self._source = source.strip().lower()

    # --------------------------------------------------------
    # source property
    # --------------------------------------------------------
    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise SmartBudgetError("Source must be a non-empty string")
        self._source = value.strip().lower()

    # --------------------------------------------------------
    # Describe
    # --------------------------------------------------------
    def describe(self) -> str:
        try:
            return (
                "Income Record\n"
                f"  Name   : {self.name}\n"
                f"  Source : {self.source}\n"
                f"  Amount : {self.amount:.2f}\n"
            )
        except Exception as e:
            raise SmartBudgetError(f"Failed to describe income: {e}")

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        try:
            return {
                "type": "Income",
                "name": self.name,
                "amount": float(self.amount),
                "source": self.source,
            }
        except Exception as e:
            raise SmartBudgetError(f"Failed to_dict Income: {e}")
