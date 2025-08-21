"""Celery worker package.

This package defines Celery tasks and serves as the entry point for
running the Celery worker.  The tasks delegate processing to use cases
defined in the shared ``packages`` package and use the dependency
injection container defined therein.
"""
