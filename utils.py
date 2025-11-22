import numpy as np
from numpy.typing import NDArray


def calculate_unit_vector(vector_x: int, vector_y: int) -> NDArray[float]:
    vector = np.array([vector_x, vector_y])
    magnitude = np.linalg.norm(vector)
    if magnitude == 0:
        return np.array([0, 0])
    else:
        return vector / magnitude
