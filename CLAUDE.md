# Development Guidelines

## Test-Driven Development (TDD)

We follow strict TDD:

1. Write a test
2. Watch it fail
3. Write code to make it pass
4. Refactor
5. Repeat

Run tests often. Keep the feedback loop tight.

## Testing Philosophy

**Test behavior, not implementation.** Tests should describe what the system does, not how it does it.

**One assertion per test.** Each test validates a single expectation. When a test fails, it should be immediately obvious what broke.

**Names matter.** Test names should clearly state the expected behavior. Reading a failing test name should tell you what went wrong without diving into the code.

**Avoid mocks when possible.** Leverage Python's dynamic nature and monkey patching. When testing responses from external libraries, use native objects from those libraries rather than generic mocks.

## Libraries and Dependencies

- Use the latest stable versions
- Prefer standard library when appropriate, but don't be dogmatic
- Well-known modern libraries are fine

## Code Style

**Optimize for vertical space.** Compact code is readable code, even if PEP8 disagrees.

Prefer one-liners:
```python
if condition: do_thing()

result = [transform(x) for x in items]
```

**Minimal exception handling.** Don't wrap everything in try/except. Let it fail. We'll fix it when we need to.

**Don't over-engineer.** This is Python, not Java:
- No excessive type hints
- No enterprise patterns for simple problems
- Keep it simple and Pythonic
