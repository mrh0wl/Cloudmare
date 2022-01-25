"""Warns on deprecated class and functions."""
import functools
import warnings
from typing import Callable, Optional


class DeprecationDecorator:
    """Deprecation Decorator for classes and functions."""

    def __init__(self, message: Optional[str] = None):
        """Inits DeprecationDecorator.

        Args:
            message (str): Optional; Message to display to user.
        """
        self.message = message

    def __call__(self, func: Callable) -> Callable:
        """Wrapper function.

        Args:
            func (Callable): Function to wrap.

        Returns:
            Callable: Wrapped function.
        """

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            # warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(
                self.message or f"Call to deprecated function {func.__name__}.",
                category=DeprecationWarning,
                stacklevel=2,
            )
            # warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        return new_func
