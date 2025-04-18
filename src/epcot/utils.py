"""Utility functions for EPCOT."""

import re


def pascal_to_kebab(pascal_case: str) -> str:
    """Convert a PascalCase string to kebab-case.

    Args:
        pascal_case: The PascalCase string to convert.

    Returns:
        The kebab-case version of the string.

    Examples:
        >>> pascal_to_kebab("MediaServer")
        'media-server'
        >>> pascal_to_kebab("ReverseProxy")
        'reverse-proxy'
        >>> pascal_to_kebab("Backup")
        'backup'
        >>> pascal_to_kebab("DNS")
        'dns'
        >>> pascal_to_kebab("IPTables")
        'ip-tables'
    """
    # Handle special cases for acronyms
    # First, handle consecutive capital letters (acronyms)
    # Replace patterns like "IP" with "Ip" to treat them as a single word
    processed = re.sub(
        r"([A-Z])([A-Z]+)(?=[A-Z][a-z]|$)",
        lambda m: m.group(1) + m.group(2).lower(),
        pascal_case,
    )

    # Then insert a hyphen before each capital letter (except the first one)
    # and convert to lowercase
    kebab_case = re.sub(r"(?<!^)(?=[A-Z])", "-", processed).lower()
    return kebab_case
