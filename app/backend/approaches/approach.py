class Approach:
    """Base class for all approaches."""
    def run(self, q: str, use_summaries: bool) -> any:
        raise NotImplementedError
