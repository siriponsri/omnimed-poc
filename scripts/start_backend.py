"""Start the M0 API with a validated local or Railway-provided port."""

import os
import sys
from collections.abc import Mapping
from typing import NoReturn

from app.config import ConfigurationError, load_settings


def runtime_port(environ: Mapping[str, str] | None = None) -> int:
    source = os.environ if environ is None else environ
    raw_port = source.get("PORT", "8000")
    if len(raw_port) > 5 or not raw_port.isascii() or not raw_port.isdecimal():
        raise ConfigurationError("PORT must be an integer between 1 and 65535.")
    port = int(raw_port)
    if not 1 <= port <= 65535:
        raise ConfigurationError("PORT must be an integer between 1 and 65535.")
    return port


def launch_arguments(port: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:create_app",
        "--factory",
        "--host",
        "0.0.0.0",  # noqa: S104 - Container ingress requires a wildcard bind.
        "--port",
        str(port),
        "--no-access-log",
        "--no-server-header",
    ]


def main() -> NoReturn:
    try:
        load_settings()
        port = runtime_port()
    except ConfigurationError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from None
    # Replace this process so container signals reach Uvicorn directly.
    os.execv(sys.executable, launch_arguments(port))  # noqa: S606 - Fixed executable and arguments.


if __name__ == "__main__":
    main()
