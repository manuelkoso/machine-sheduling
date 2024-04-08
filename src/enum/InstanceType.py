from enum import Enum


class InstanceType(Enum):
    SYNTHETIC = "synthetic"
    REAL = "real"

    def __str__(self):
        return str(self.value)
