import random
from collections import defaultdict


class ThresholdSelector:
    def __init__(self, seed: int, thresholds: dict[str, float]):
        self.seed = seed
        self.thresholds = (
            thresholds  # ex: {"common": 0.3, "rare": 0.7, "legendary": 0.9}
        )

    def threshold_selection(
        self, value: float, option_labels: dict[str, str], seed: int = None
    ) -> str:
        if seed is None:
            seed = self.seed
        # option_labels = {"wood": "common", "gold": "rare", ...}
        label_groups = defaultdict(list)
        for option, label in option_labels.items():
            label_groups[label].append(option)

        sorted_thresholds = sorted(
            self.thresholds.items(), key=lambda x: x[1], reverse=True
        )
        for label, threshold in sorted_thresholds:
            if value >= threshold and label in label_groups:
                label_seed = hash((seed, label))
                rng = random.Random(label_seed)
                return rng.choice(label_groups[label])

        fallback_label = min(self.thresholds.items(), key=lambda x: x[1])[0]
        return random.Random(seed).choice(label_groups[fallback_label])

    def weighted_selection(self, value: float, option_labels: dict[str, str]) -> str:
        # Weight = inverse of threshold distance to 0, fallback to 1.0 if unknown
        label_weights = {
            label: 1.0 / (1e-6 + threshold)
            for label, threshold in self.thresholds.items()
        }

        weighted = [
            (opt, label_weights.get(label, 1.0)) for opt, label in option_labels.items()
        ]
        total = sum(w for _, w in weighted)
        normalized = [(opt, w / total) for opt, w in weighted]

        cumulative = 0
        for opt, weight in normalized:
            cumulative += weight
            if value <= cumulative:
                return opt
        return normalized[-1][0]
