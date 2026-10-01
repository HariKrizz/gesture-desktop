from app.config.settings import PINCH_THRESHOLD


def is_pinching(distance):
    return distance < PINCH_THRESHOLD

