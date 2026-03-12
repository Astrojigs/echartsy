"""Custom exceptions and warnings for echartslib."""


class BuilderError(Exception):
    """Base exception for all builder-related errors."""


class BuilderConfigError(BuilderError):
    """Raised when the builder receives contradictory or invalid configuration.

    Example
    -------
    >>> fig = Figure()
    >>> fig.pie(df, names="A", values="B").xlim(0, 10)
    BuilderConfigError: xlim() is not applicable to pie charts.
    """


class DataValidationError(BuilderError):
    """Raised when input data is missing expected columns or has wrong dtypes.

    Example
    -------
    >>> fig = Figure()
    >>> fig.bar(df, x="nonexistent_col", y="Revenue")
    DataValidationError: Column 'nonexistent_col' not found in DataFrame.
    """


class TimelineConfigError(BuilderConfigError):
    """Raised when TimelineFigure configuration is invalid."""


class OverlapWarning(UserWarning):
    """Non-fatal warning emitted when the layout resolver detects potential overlap.

    The resolver will auto-fix the issue (rotate labels, expand margins, etc.)
    and emit this warning so callers know an adjustment was made.
    """
