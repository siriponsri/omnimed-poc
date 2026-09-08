"""Port validation and launch settings used by both Docker Compose and Railway."""

import pytest

from app.config import ConfigurationError
from scripts.start_backend import launch_arguments, runtime_port


@pytest.mark.parametrize("port", ["", "0", "65536", "-1", "80.5", " 8000 ", "eight", "８０００"])
def test_invalid_runtime_ports_fail_before_launch(port: str) -> None:
    with pytest.raises(ConfigurationError, match="PORT must be an integer"):
        runtime_port({"PORT": port})


def test_runtime_port_uses_local_default_and_railway_override() -> None:
    assert runtime_port({}) == 8000
    assert runtime_port({"PORT": "43210"}) == 43210
    assert runtime_port({"PORT": "1"}) == 1
    assert runtime_port({"PORT": "65535"}) == 65535


def test_runtime_port_error_does_not_echo_untrusted_input() -> None:
    with pytest.raises(ConfigurationError) as error:
        runtime_port({"PORT": "private-input-sentinel"})
    assert "private-input-sentinel" not in str(error.value)


def test_oversized_numeric_port_is_rejected_before_integer_conversion() -> None:
    with pytest.raises(ConfigurationError):
        runtime_port({"PORT": "9" * 10000})


def test_launch_uses_factory_runtime_port_and_no_access_logs() -> None:
    arguments = launch_arguments(43210)
    assert arguments[1:4] == ["-m", "uvicorn", "app.main:create_app"]
    assert arguments[arguments.index("--port") + 1] == "43210"
    assert arguments[arguments.index("--host") + 1] == "0.0.0.0"  # noqa: S104 - Container bind.
    assert "--factory" in arguments
    assert "--no-access-log" in arguments
    assert "--no-server-header" in arguments
