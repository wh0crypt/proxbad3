import json
import os

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


CONFIG_FILE = os.path.expanduser("~/.proxbad3_config.json")


class Config:
    """Configuration class to hold the selected device and frequency mode."""

    def __init__(
        self, device: str | None = None, freq: Frequency = Frequency.NONE
    ) -> None:
        self.device = device if device is not None else None
        self.freq = freq

    def load(self) -> None:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.device = data.get("device", None)
                    freq_name = data.get("freq", "NONE")
                    try:
                        self.freq = Frequency[freq_name]
                    except KeyError:
                        self.freq = Frequency.NONE
            except Exception:
                self.device = None
                self.freq = Frequency.NONE

    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(
                {
                    "device": (
                        self.device.split(" - ")[0]
                        if isinstance(self.device, str)
                        else None
                    ),
                    "freq": self.freq.name,
                },
                f,
                indent=4,
            )
