import numpy as np
from numpy.typing import NDArray


class Model:
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.entities: list[ModelEntity] = []

        print("Initialized model")

    def update_model(self, dt: float) -> None:
        for entity in self.entities:
            entity.update(dt)


class ModelEntity:
    def __init__(
        self,
        width: float = 10.0,
        height: float = 10.0,
        start_pos: NDArray[float] = np.array([0, 0]),
        start_v: NDArray[float] = np.array([0, 0]),
        start_a: NDArray[float] = np.array([0, 0]),
        velocity_limit: float = 2.0,
    ):
        self.width: float = width
        self.height: float = height
        self.position: NDArray[float] = start_pos
        self.velocity: NDArray[float] = start_v
        self.acceleration: NDArray[float] = start_a
        self.max_velocity: float = velocity_limit

    def update(self, dt: float) -> None:
        self.velocity += self.acceleration
        self.limit_velocity()
        self.position += self.velocity
        self.acceleration = np.array([0, 0])

    def limit_velocity(self):
        magnitude = np.linalg.norm(self.velocity)
        if magnitude > self.max_velocity:
            self.velocity = self.velocity / magnitude
