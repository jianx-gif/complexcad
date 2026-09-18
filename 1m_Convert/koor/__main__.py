"""Allow ``python -m koor ...`` as an alias of the ``koor`` console script."""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
