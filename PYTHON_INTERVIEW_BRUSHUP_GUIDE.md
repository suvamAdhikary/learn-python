# Python Interview Brush-Up Guide

This guide is a practical roadmap for the topics in your checklist, with concise explanations and interview-style examples.

---

## 1) Data Structures & Algorithms

### Arrays (Python `list`)
- Dynamic array under the hood.
- Fast index access `O(1)`.
- Append is amortized `O(1)`.
- Insert/delete in the middle is `O(n)` due to shifting.

```python
nums = [10, 20, 30]
nums.append(40)      # [10, 20, 30, 40]
print(nums[1])       # 20
```

### Dicts (`dict`)
- Hash table: average `O(1)` insert/lookup/delete.
- Keys must be hashable (`str`, `int`, tuples of immutables, etc.).

```python
user = {"id": 1, "name": "Ada"}
print(user["name"])           # Ada
user["role"] = "engineer"
```

### Sets (`set`)
- Unique elements only.
- Average `O(1)` membership checks.

```python
seen = {1, 2, 3}
print(2 in seen)       # True
seen.add(4)
```

### Heaps (`heapq`)
- Binary min-heap.
- `heappush` / `heappop` are `O(log n)`.
- Great for top-k / priority scheduling.

```python
import heapq
h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappush(h, 3)
print(heapq.heappop(h))   # 1
```

### Sorting
- Python uses Timsort (`O(n log n)` worst case, very good for partially sorted data).
- Stable sort: equal keys keep original order.

```python
people = [("a", 30), ("b", 20), ("c", 20)]
print(sorted(people, key=lambda x: x[1]))
# [('b', 20), ('c', 20), ('a', 30)]  <- b stays before c
```

### Sliding Window
Use for contiguous subarray/substring constraints.

```python
# Longest substring without repeating characters

def longest_unique(s: str) -> int:
    left = 0
    seen = {}
    best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

### Two Pointers
Use when processing sorted arrays or opposite-end checks.

```python
# Pair sum in sorted array

def has_pair(nums, target):
    i, j = 0, len(nums) - 1
    while i < j:
        total = nums[i] + nums[j]
        if total == target:
            return True
        if total < target:
            i += 1
        else:
            j -= 1
    return False
```

---

## 2) Language Internals

### List vs Generator vs Iterator
- **List**: stores all values in memory.
- **Generator**: lazy sequence via `yield`.
- **Iterator**: object implementing `__iter__` + `__next__`.

```python
lst = [x * x for x in range(5)]        # list: eager

gen = (x * x for x in range(5))        # generator: lazy
print(next(gen))                       # 0
print(next(gen))                       # 1
```

### Mutable Default Args Pitfall
Bad:

```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket
```

Good:

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

### Shallow vs Deep Copy
- `copy.copy`: copies outer container, nested references shared.
- `copy.deepcopy`: recursively copies nested objects.

```python
import copy

a = [[1, 2], [3, 4]]
b = copy.copy(a)
c = copy.deepcopy(a)

a[0].append(99)
print(b)  # [[1, 2, 99], [3, 4]]  (shared inner list)
print(c)  # [[1, 2], [3, 4]]
```

---

## 3) OOP & Patterns

### Class vs Dataclass
Use `@dataclass` for data containers (less boilerplate).

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
```

Choose regular class when you need custom lifecycle/behavior-heavy logic.

### Inheritance vs Composition
- **Inheritance**: "is-a" relationship.
- **Composition**: "has-a" relationship; often more flexible and testable.

```python
class Engine:
    def start(self):
        return "engine started"

class Car:
    def __init__(self, engine: Engine):
        self.engine = engine
```

### Factory Pattern
Encapsulates object creation logic.

```python
class JsonParser: ...
class XmlParser: ...

def parser_factory(kind: str):
    if kind == "json":
        return JsonParser()
    if kind == "xml":
        return XmlParser()
    raise ValueError("unknown parser")
```

### Dependency Injection (DI) Basics
Inject dependencies instead of hardcoding them.

```python
class EmailService:
    def send(self, msg):
        ...

class Notification:
    def __init__(self, service: EmailService):
        self.service = service
```

Benefits: easier testing (swap real service with mock/fake).

---

## 4) Concurrency

### GIL Implications
- CPython has a Global Interpreter Lock.
- Only one thread executes Python bytecode at a time.
- Threads help mostly with I/O-bound tasks, not CPU-bound parallel speedup.

### Threading vs Multiprocessing vs Asyncio
- **threading**: best for I/O-bound work with blocking APIs.
- **multiprocessing**: CPU-bound parallelism using multiple processes.
- **asyncio**: high-concurrency I/O when libraries are async-friendly.

Quick rule:
- CPU-heavy image processing? `multiprocessing`.
- Many network calls? `asyncio`.
- Existing blocking code + simple concurrency? `threading`.

---

## 5) Common Libraries

### `collections`
- `deque`: fast append/pop from both ends.
- `defaultdict`: automatic default values.
- `Counter`: count hashable items.

```python
from collections import deque, defaultdict, Counter

dq = deque([1, 2]); dq.appendleft(0)
by_letter = defaultdict(list); by_letter['a'].append('apple')
freq = Counter("banana")
```

### `itertools`
Efficient iterator building blocks.

```python
from itertools import combinations
print(list(combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]
```

---

## 6) Interview Problem: Flatten Nested Integers Iterator

Given a nested list like:

```python
[1, [2, [3, 4], 5], 6]
```

build an iterator that returns values one-by-one as:

```text
1, 2, 3, 4, 5, 6
```

Use a stack to avoid recursion limits and keep iteration lazy.

```python
from collections.abc import Iterator


class NestedIterator(Iterator[int]):
    def __init__(self, nested_list):
        self._stack = [iter(nested_list)]
        self._next_val = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_val is None and not self._advance():
            raise StopIteration

        value = self._next_val
        self._next_val = None
        return value

    def _advance(self):
        while self._stack:
            try:
                item = next(self._stack[-1])
            except StopIteration:
                self._stack.pop()
                continue

            if isinstance(item, int):
                self._next_val = item
                return True

            self._stack.append(iter(item))

        return False


# Example usage
nested = [1, [2, [3, 4], 5], 6]
print(list(NestedIterator(nested)))
# [1, 2, 3, 4, 5, 6]
```

Time complexity: `O(n)` total for `n` integers/lists visited.  
Space complexity: `O(d)` where `d` is max nesting depth (stack of iterators).

### `functools.lru_cache`
Memoization decorator for pure functions.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

### `asyncio` and `concurrent.futures`
- `asyncio.gather` for concurrent coroutines.
- `ThreadPoolExecutor` / `ProcessPoolExecutor` for pool-based parallelism.

---

## 6) Practical Topics

### Memoization
Store previous results to avoid repeated computation.
- Manual dict cache or `@lru_cache`.

### Decorators
Wrap functions to add reusable behavior.

```python
def log_calls(fn):
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper
```

### Context Managers
Use `with` for deterministic setup/cleanup.

```python
with open("data.txt") as f:
    data = f.read()
```

### Exception Handling
- Catch specific exceptions.
- Avoid bare `except:`.
- Add context in logs/errors.

### Logging
Prefer `logging` over `print` in production.

```python
import logging
logging.basicConfig(level=logging.INFO)
logging.info("service started")
```

### Profiling (`cProfile`, `timeit`)

```bash
python -m cProfile app.py
python -m timeit "sum(range(1000))"
```

---

## 7) Production Topics

### Packaging
- Modern standard: `pyproject.toml`.
- Tools: `setuptools`, `poetry`, `hatch`, etc.

### Virtualenv
- Isolate project dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
```

### `requirements.txt` vs `pyproject.toml`
- `requirements.txt`: pinned environment dependencies.
- `pyproject.toml`: project metadata + dependency declarations.

### CI
- Run lint, type-check, tests on each PR.
- Common with GitHub Actions.

### Type Hints + `mypy`

```python
def add(a: int, b: int) -> int:
    return a + b
```

Run:

```bash
mypy your_package/
```

### Observability
- **Logging**: structured logs.
- **Metrics**: latency, error rate, throughput.
- **Tracing** (advanced): request flow across services.

---

## 8) Interview Prep Plan (4 Weeks)

### Week 1: DSA + Python core
- Arrays/dicts/sets/heaps/sorting.
- Sliding window + two pointers (5 problems each).
- Review mutability, iterators/generators.

### Week 2: OOP + practical Python
- Dataclass/class, composition, factory, DI.
- Decorators/context managers/exceptions/logging.
- Write one small CLI project.

### Week 3: Concurrency + libraries
- Threading/multiprocessing/asyncio side-by-side examples.
- Practice `collections`, `itertools`, `lru_cache`.

### Week 4: Production readiness + mock interviews
- Packaging + venv + mypy + basic CI pipeline.
- 6–8 mock interview problems with explanation out loud.

---

## 9) Practice Prompts (Interview Style)

1. Explain why dict lookup is average `O(1)` and when it degrades.
2. When would you use a generator over a list?
3. Why is mutable default arg dangerous? Show fix.
4. Composition vs inheritance: give real project example.
5. How does GIL affect CPU-bound threads?
6. How would you debug a slow Python API endpoint?
7. Difference between `requirements.txt` and `pyproject.toml`?

---

## 10) Suggested Next Steps

- Solve 2 DSA problems daily (1 sliding window, 1 two pointers every other day).
- Build one mini-project combining:
  - logging
  - type hints
  - async or threads
  - packaging with `pyproject.toml`
- Practice explaining trade-offs out loud (interviews value this heavily).
