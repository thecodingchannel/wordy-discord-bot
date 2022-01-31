from __future__ import annotations

import os
import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TypeVar, cast


TResult = TypeVar('TResult')
NO_CACHE = object()

_file_caches = {}


@dataclass
class FileLoaderState:
    path: str
    ctime: float = 0
    mtime: float = 0
    size: int = 0
    cache: Any = NO_CACHE


def cache_file(path: str) -> Callable[[Callable[[bytes], TResult]], Callable[[], TResult]]:
    '''
    A decorator that runs a function with file contents loaded from disk, but only
    if the file has changed since the last time it was read, else the cached
    result is returned.
    '''
    def cache_file_inner(func):
        @functools.wraps(func)
        def wrapper():
            state = _file_caches.setdefault(path, FileLoaderState(path))
            if _should_fetch_file(state):
                data = _read_file(state)
                state.cache = func(data)

            return state.cache

        return wrapper

    return cache_file_inner


def fetch_cached_file(path: str, transform_fn: Callable[[bytes], TResult]) -> TResult:
    '''
    Fetch a file from disk, transforming it using the given function and caching the result.
    Cached data is used if available and the file on disk is unchanged, skipping the transform stage.
    '''
    state = _file_caches.setdefault(path, FileLoaderState(path))
    if _should_fetch_file(state):
        data = _read_file(state)
        state.cache = transform_fn(data)

    return cast(Any, state.cache)


def _should_fetch_file(state: FileLoaderState) -> bool:
    '''
    Works out if a file needs to be fetched from disk.

    This happens when it is not previously cache, or
    when the file has been modified since on disk.
    '''
    # Not cached already?
    if state.cache is NO_CACHE:
        return True

    # Has the file changed?
    stat = os.stat(state.path)
    if state.ctime != stat.st_ctime:
        return True
    if state.mtime != stat.st_mtime:
        return True
    if state.size != stat.st_size:
        return True

    # Then use the cache
    return False


def _read_file(state: FileLoaderState) -> bytes:
    print(f"Reading file: {state.path}")
    stat = os.stat(state.path)
    state.ctime = stat.st_ctime
    state.mtime = stat.st_mtime
    state.size = stat.st_size
    return Path(state.path).read_bytes()

