"""Tiny module under test — keep the focus on the pipeline."""


def hello() -> str:
    # Intentional mismatch with tests/test_hello.py so the first Actions run fails.
    # Challenge 0: make CI green (change this return value or the test expectation).
    return "Hello, Actions!"


if __name__ == "__main__":
    print(hello())
