"""Test that debug mode correctly suppresses errors in the CLI."""

# Future imports
from __future__ import annotations

# Standard library imports
from pathlib import Path
from typing import (
    Callable,  # Import from collections.abc in Python 3.9
    List,  # Not needed in Python 3.9
    Tuple,  # Not needed in Python 3.9
    Optional,  # Not needed in Python 3.10
    )

# Third party imports
import pytest
from _pytest.capture import (
    CaptureResult,
    )
from typing_extensions import (
    Final,  # Added to typing in Python 3.8
    )

# Local imports
import submanager.core.initialization
import submanager.models.config


# ---- Types ----

RunCLICallable = Callable[
    [List[str]], Tuple[CaptureResult[str], Optional[SystemExit]]]


# ---- Constants ----

GENERATE_COMMAND: Final[str] = "generate-config"


# ---- Helpers ----

def render_generate_args(config_path: Path, *args: str) -> list[str]:
    """Render the appropriate CLI args for the generate command."""
    args = tuple((arg for arg in args if arg))
    return ["--config-path", config_path.as_posix(), "generate-config", *args]


# ---- Tests ----

@pytest.mark.parametrize("force_arg", ["", "--force"])
@pytest.mark.parametrize("exist_ok_arg", ["", "--exist-ok"])
def test_config_doesnt_exist(
        run_cli: RunCLICallable,
        config_paths: submanager.models.config.ConfigPaths,
        force_arg: str,
        exist_ok_arg: str,
        ) -> None:
    """Test that the config file is generated when one doesn't exist."""
    cli_args = render_generate_args(
        config_paths.static, force_arg, exist_ok_arg)
    captured_output, captured_error = run_cli(cli_args)
    assert not captured_output.err.strip()
    assert not captured_error
    assert captured_output.out.strip()
    assert "generated" in captured_output.out.lower()
    assert config_paths.static.exists()
    submanager.core.initialization.setup_config(config_paths, verbose=True)
