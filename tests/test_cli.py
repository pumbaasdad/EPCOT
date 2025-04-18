"""Tests for the cli module."""

import pytest
from pathlib import Path
import tempfile
import yaml
from typing import Generator
from unittest.mock import patch, MagicMock

from epcot.cli import (
    validate_figments_list,
    validate_figment_name,
    to_pascal_case,
    get_figment_class,
    main,
)
from epcot.figment import Figment


def test_validate_figments_list_valid() -> None:
    """Test validating a valid figments list."""
    figments = ["backup", "certificates", {"reverse-proxy": {"key": "value"}}]
    result = validate_figments_list(figments)
    assert result == figments


def test_validate_figments_list_not_list() -> None:
    """Test validating a figments value that is not a list."""
    with pytest.raises(ValueError, match="figments must be a list"):
        validate_figments_list({"not": "a list"})


def test_validate_figments_list_invalid_item() -> None:
    """Test validating a figments list with an invalid item."""
    with pytest.raises(ValueError, match="figment must be a string or dictionary"):
        validate_figments_list(["backup", 123])


def test_validate_figments_list_invalid_dict() -> None:
    """Test validating a figments list with an invalid dictionary."""
    with pytest.raises(
        ValueError, match="figment dictionary must have exactly one key"
    ):
        validate_figments_list(["backup", {"key1": "value1", "key2": "value2"}])


def test_validate_figment_name_valid() -> None:
    """Test validating a valid figment name."""
    name = "reverse-proxy"
    result = validate_figment_name(name)
    assert result == name


def test_validate_figment_name_invalid() -> None:
    """Test validating an invalid figment name."""
    with pytest.raises(ValueError, match="figment name must be in kabab-case"):
        validate_figment_name("ReverseProxy")


def test_to_pascal_case() -> None:
    """Test converting a kabab-case string to PascalCase."""
    assert to_pascal_case("reverse-proxy") == "ReverseProxy"
    assert to_pascal_case("backup") == "Backup"
    assert to_pascal_case("media-server-config") == "MediaServerConfig"


class MockFigment(Figment):
    """Mock figment class for testing."""


class NotAFigment:
    """Class that does not inherit from Figment."""

    pass


@patch("importlib.import_module")
def test_get_figment_class_success(mock_import: MagicMock) -> None:
    """Test getting a figment class successfully."""
    mock_module = MagicMock()
    mock_module.TestFigment = MockFigment
    mock_import.return_value = mock_module

    figment_class = get_figment_class("test-figment")
    assert figment_class == MockFigment
    mock_import.assert_called_once_with("epcot.figments.test_figment")


@patch("importlib.import_module")
def test_get_figment_class_import_error(mock_import: MagicMock) -> None:
    """Test getting a figment class with an import error."""
    mock_import.side_effect = ImportError("Module not found")

    with pytest.raises(ImportError, match="Could not import figment module"):
        get_figment_class("test-figment")


@patch("importlib.import_module")
def test_get_figment_class_attribute_error(mock_import: MagicMock) -> None:
    """Test getting a figment class with an attribute error."""
    mock_module = MagicMock()
    mock_module.TestFigment = None
    mock_import.return_value = mock_module

    with pytest.raises(TypeError, match="Figment class must be a class"):
        get_figment_class("test-figment")


@patch("importlib.import_module")
def test_get_figment_class_not_a_figment(mock_import: MagicMock) -> None:
    """Test getting a class that does not inherit from Figment."""
    mock_module = MagicMock()
    mock_module.TestFigment = NotAFigment
    mock_import.return_value = mock_module

    with pytest.raises(TypeError, match="Figment class must inherit from Figment"):
        get_figment_class("test-figment")


@pytest.fixture
def config_file() -> Generator[Path, None, None]:
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as temp:
        yaml.dump(
            {
                "figments": [
                    "backup",
                    "certificates",
                    {"reverse-proxy": {"key": "value"}},
                ]
            },
            temp,
        )
        yield Path(temp.name)


@patch("epcot.cli.get_figment_class")
@patch("epcot.cli.Path")
def test_main_success(
    mock_path: MagicMock, mock_get_class: MagicMock, config_file: Path
) -> None:
    """Test the main function with a successful execution."""
    mock_path.return_value = config_file
    mock_figment = MagicMock()
    mock_figment_class = MagicMock(return_value=mock_figment)
    mock_get_class.return_value = mock_figment_class

    result = main()

    assert result == 0
    assert mock_get_class.call_count == 3


@patch("epcot.cli.Path")
def test_main_no_figments(mock_path: MagicMock, config_file: Path) -> None:
    """Test the main function with no figments in the config."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as temp:
        yaml.dump({}, temp)
        mock_path.return_value = Path(temp.name)

    result = main()

    assert result == 1


@patch("epcot.cli.Path")
def test_main_error(mock_path: MagicMock) -> None:
    """Test the main function with an error."""
    mock_path.return_value = Path("non_existent_file.yaml")

    result = main()

    assert result == 1
