from __future__ import annotations

import typer


def validate_positive_integer(value: int, field_name: str) -> int:
    """Validate that a CLI integer option is greater than zero.
    
    Args:
        value: Option value provided by the user
        field_name: Human-readable option name for error messages
        
    Returns:
        The validated positive integer
        
    Raises:
        typer.BadParameter: If value is less than 1
    """
    if value < 1:
        raise typer.BadParameter(f"{field_name} must be at least 1.")
    return value


def validate_refresh_interval(value: int) -> int:
    """Validate the monitor refresh interval."""
    return validate_positive_integer(value, "Refresh interval")
