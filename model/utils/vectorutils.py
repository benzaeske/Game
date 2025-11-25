from pygame import Vector2


def limit_magnitude(vec: Vector2, limit: float) -> None:
    """
    A safe way of calling pygame.clamp_magnitude_ip on the provided Vector2 that does not throw an error if the magnitude is 0.\n
    If the magnitude of the input vector is 0 this function does nothing
    """
    if vec.magnitude() != 0.0:
        vec.clamp_magnitude_ip(limit)


def safe_normalize(vec: Vector2) -> None:
    """
    A safe way of calling pygame.normalize_ip on the provided Vector2 that does not throw an error if the magnitude is 0.\n
    If the magnitude of the input vector is 0 this function does nothing
    """
    if vec.magnitude() != 0.0:
        vec.normalize_ip()
