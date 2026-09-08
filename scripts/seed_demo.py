"""Run an explicit synthetic fixture seed without revealing connection details."""

import sys

from sqlalchemy.exc import SQLAlchemyError

from app.config import ConfigurationError, load_settings
from app.database import build_engine
from app.foundation.seed import SeedConflict, seed_demo


def main() -> int:
    try:
        settings = load_settings()
        engine = build_engine(settings)
        try:
            summary = seed_demo(engine)
        finally:
            engine.dispose()
    except (ConfigurationError, SeedConflict, SQLAlchemyError):
        print(
            "Seed failed. Check local configuration, migrated schema and fixture integrity. "
            "No partial seed was committed.",
            file=sys.stderr,
        )
        return 1
    print(summary.model_dump_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
