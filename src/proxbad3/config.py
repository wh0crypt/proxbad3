from enum import Enum


class Frequency(Enum):
    """Enumeration for supported frequency modes."""

    HF = 0
    LF = 1
    NONE = 2

    @classmethod
    def _missing_(cls, value):
        """Handle missing values gracefully."""
        if value is None:
            return cls.NONE
        return cls.NONE


class Config:
    """Configuration class to hold the selected device and frequency mode."""

    def __init__(self, device: str | None, freq: Frequency) -> None:
        self.device = device
        self.freq = freq
