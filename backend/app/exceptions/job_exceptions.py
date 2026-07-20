class JobAlreadyExists(Exception):
    """Raised when attempting to save a job that is already in the database."""

    pass


class ScraperError(Exception):
    """Raised when a job scraper fails to fetch or parse data."""

    pass
