REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080

WIDTH = 1920
HEIGHT = 1080
# WIDTH = 1600
# HEIGHT = 900


def sw(value: float) -> float:
    """Scale width according to reference Full-HD width."""
    return value * (WIDTH / REFERENCE_WIDTH)


def sh(value: float) -> float:
    """Scale height according to reference Full-HD height."""
    return value * (HEIGHT / REFERENCE_HEIGHT)
