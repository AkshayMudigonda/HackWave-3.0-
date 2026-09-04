from collections import defaultdict, deque
from typing import Dict, Iterable, List


class MetricHistory:
    def __init__(self, window: int = 30):
        self.window = window
        self._values = defaultdict(lambda: deque(maxlen=window))

    def add(self, metrics: Dict[str, object]) -> None:
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                self._values[key].append(float(value))

    def values(self, metric: str) -> List[float]:
        return list(self._values[metric])
