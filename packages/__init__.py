"""Shared packages for both API and worker.

This package contains the domain, application, adapters and infrastructure
modules that are common to both the FastAPI application (`api_app`) and
Celery worker (`worker_app`).

To maintain backward compatibility with code that imports from the legacy
`app` package, this module aliases itself to the name `app` in
``sys.modules``.  This allows statements like ``from app.domain.entities import ...``
to continue working without modification, even though the actual package
name is ``packages``.

Usage:
    >>> import packages.domain.entities.mission
    >>> import app.domain.entities.mission  # resolved to packages

The aliasing is set up at import time.
"""

import sys as _sys

# Alias this package under the name 'app' for backwards compatibility.
_sys.modules.setdefault('app', _sys.modules[__name__])
