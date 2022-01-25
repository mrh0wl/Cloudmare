"""Censys Version."""
try:  # pragma: no cover
    import importlib_metadata
except ImportError:  # pragma: no cover
    import importlib.metadata as importlib_metadata  # type: ignore

__version__: str = '2.1.2'
