from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

class Result(Generic[T, E]):
    pass

@dataclass(frozen=True) # automatically gets common “data container” methods generated for you, such as __init__, __repr__, and __eq__
class Ok(Result[T, E]):
    data: T

@dataclass(frozen=True) # frozen=True makes it immutable
class Error(Result[T, E]):
    error: E


'''
Classes above mimics Rust's Result<T, E> enum.
Doesn't actually works like it in language level, only library/convention
'''