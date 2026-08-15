import pytest


def main() -> int:
    args = ["-q", "test_cases"]
    return pytest.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
