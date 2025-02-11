def safe_divide(numerator, denominator):
    """Avoid division by zero."""
    return numerator / denominator if denominator else 0
