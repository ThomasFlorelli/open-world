import hashlib
import random

from generation_config import NoiseSmoothing
from utils import interpolate


class NoiseMap:
    def __init__(
        self,
        seed: int = 0,
        scale: int = 10,
        smoothing: NoiseSmoothing = NoiseSmoothing.LINEAR,
    ):
        self.seed = seed
        self.scale = scale
        self.smoothing = smoothing

    def apply_noise_smoothing(self, value: float) -> float:
        # Clamp to [0,1]
        value = max(0.0, min(1.0, (value + 1) / 2))  # Map from [-1,1] to [0,1]

        if self.smoothing == NoiseSmoothing.FAVOR_COMMON:
            return pow(value, 2.2)
        elif self.smoothing == NoiseSmoothing.FAVOR_RARE:
            return 1 - pow(1 - value, 2.2)
        return value  # LINEAR or fallback

    def hash_noise(self, x, y, seed):
        key = f"{x},{y},{seed}".encode()
        h = hashlib.sha256(key).digest()
        return h[0] / 255

    def generate_global_noise(self, x, y, seed=None) -> float:
        if seed is None:
            seed = self.seed
        gx, gy = x // self.scale, y // self.scale
        fx, fy = (x % self.scale) / self.scale, (y % self.scale) / self.scale

        a = self.hash_noise(gx, gy, seed)
        b = self.hash_noise(gx + 1, gy, seed)
        c = self.hash_noise(gx, gy + 1, seed)
        d = self.hash_noise(gx + 1, gy + 1, seed)

        top = interpolate(a, b, fx)
        bottom = interpolate(c, d, fx)
        return interpolate(top, bottom, fy)

    def generate_local_noise(
        self, width: int, height: int, seed: int = None
    ) -> list[list[float]]:
        if seed is None:
            seed = self.seed

        rng = random.Random(seed)
        grid_width = width // self.scale + 2
        grid_height = height // self.scale + 2

        grid = [[rng.random() for _ in range(grid_width)] for _ in range(grid_height)]
        noise = [[0.0 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                gx, gy = x // self.scale, y // self.scale
                fx, fy = (x % self.scale) / self.scale, (y % self.scale) / self.scale

                top = interpolate(grid[gy][gx], grid[gy][gx + 1], fx)
                bottom = interpolate(grid[gy + 1][gx], grid[gy + 1][gx + 1], fx)
                noise[y][x] = interpolate(top, bottom, fy)

        return noise
