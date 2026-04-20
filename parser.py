"""
Configuration parsing pipeline for A-Maze-Ing.

This module handles the full lifecycle of reading and validating the
configuration file passed on the command line:
- validates that exactly one CLI argument (the config file path) was given
- reads the file from disk
- parses KEY=VALUE lines while ignoring blanks and comments
- type-converts and validates each value
- returns a ready-to-use configuration dictionary to the caller
"""
import sys


REQUIRED_KEYS: list = [
    "width",
    "height",
    "entry",
    "exit",
    "output_file",
    "perfect"
]


def validate_args() -> str:
    """
    Validate command-line arguments and return the config file path.

    This function checks whether the program was called with exactly one
    argument besides the script name. That argument must be the path to
    the configuration file.

    Returns:
        str: The path to the configuration file.

    Raises:
        SystemExit: If the number of arguments is invalid.
    """
    if len(sys.argv) != 2:
        print("Error: correct use python3 a_maze_ing.py config.txt")
        sys.exit(1)
    cfg_path = sys.argv[1]
    return cfg_path


def load_config_file(cfg_path: str) -> list:
    """
    Open and read the configuration file.

    This function reads the file located at `cfg_path` and returns all
    lines as a list of strings.

    Args:
        cfg_path (str): Path to the configuration file.

    Returns:
        list[str]: A list containing all lines of the file.

    Raises:
        SystemExit: If the file does not exist or cannot be read due to
            permission errors.
    """
    try:
        with open(cfg_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found {cfg_path}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {cfg_path}")
        sys.exit(1)
    return lines


def parse_config_lines(lines: list) -> dict:
    """
    Parse raw configuration lines into a dictionary.

    This function processes each line of the configuration file, ignoring
    empty lines and comments. Valid lines must follow the format KEY=VALUE.

    It also checks for:
    - invalid line format
    - empty keys
    - empty values
    - duplicated keys

    Args:
        lines (list[str]): List of lines read from the configuration file.

    Returns:
        dict[str, str]: Dictionary mapping configuration keys to raw string
        values.

    Raises:
        ValueError: If a line has invalid syntax, an empty key/value,
            or a duplicated key.
    """
    raw_config = {}

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        if not line or line.startswith('#'):
            continue
        elif line and '#' in line:
            line = line.split('#')[0]

        parts: list = line.split('=')
        if len(parts) != 2:
            raise ValueError(f"Line {line_number}: invalid format")

        key = parts[0].strip().lower()
        value = parts[1].strip()

        if not key:
            raise ValueError(f"Line {line_number}: Empty key")
        if not value:
            raise ValueError(f"Line {line_number}: Empty value")
        if key in raw_config:
            raise ValueError(f"Line {line_number}: Duplicated key {key}")

        raw_config[key] = value
    return raw_config


def validate_required_keys(raw_config: dict) -> None:
    """
    Check whether all mandatory configuration keys are present.

    The required keys are defined in the global REQUIRED_KEYS list.

    Args:
        raw_config (dict[str, str]): Dictionary containing parsed raw config
        values.

    Raises:
        ValueError: If any required key is missing.
    """
    for key in REQUIRED_KEYS:
        if key not in raw_config:
            raise ValueError(f"Missing key: {key}")


def parse_int(value: str, key_name: str) -> int:
    """
    Convert a configuration value to an integer.

    Args:
        value (str): The raw value to convert.
        key_name (str): Name of the configuration key, used in error messages.

    Returns:
        int: The converted integer value.

    Raises:
        ValueError: If the value cannot be converted to an integer.
    """
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{key_name} must be a valid integer")


def parse_coordinates(value: str, key_name: str) -> tuple:
    """
    Parse a coordinate string in the format 'x,y'.

    This function splits the input string using ',' and converts both
    parts into integers.

    Args:
        value (str): Coordinate value as a string, expected in the format
        'x,y'.
        key_name (str): Name of the configuration key, used in error messages.

    Returns:
        tuple[int, int]: A tuple (x, y) with integer coordinates.

    Raises:
        ValueError: If the format is invalid or if x/y are not integers.
    """
    parts = value.split(',')
    if len(parts) != 2:
        raise ValueError(f"{key_name} must be in format x,y")
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        raise ValueError(f"{key_name} must contain valid integers")
    return (x, y)


def parse_bool(value: str, key_name: str) -> bool:
    """
    Convert a configuration value to a boolean.

    Only the strings 'True' and 'False' are accepted.

    Args:
        value (str): The raw value to convert.
        key_name (str): Name of the configuration key, used in error messages.

    Returns:
        bool: True if value is 'True', False if value is 'False'.

    Raises:
        ValueError: If the value is not exactly 'True' or 'False'.
    """
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"{key_name} must be True or False")


def validate_bounds(
    point: tuple,
    width: int,
    height: int,
    key_name: str
) -> None:
    """
    Check whether a coordinate is inside maze bounds.

    Args:
        point (tuple[int, int]): Tuple (x, y) representing a position in the
        maze.
        width (int): Maze width.
        height (int): Maze height.
        key_name (str): Name of the configuration key, used in error messages.

    Raises:
        ValueError: If the point is outside the maze boundaries.
    """
    x, y = point
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"{key_name} out of limits")


def build_and_validate_config(raw_config: dict) -> dict:
    """
    Convert raw configuration values into validated typed data.

    This function:
    - checks that all required keys exist
    - converts values to their expected types
    - validates numeric limits and coordinate bounds
    - checks that ENTRY and EXIT are different
    - optionally parses SEED if present

    Args:
        raw_config (dict[str, str]): Dictionary of raw string values from the
        parser.

    Returns:
        dict[str, object]: Final validated configuration dictionary with
        proper types.

    Raises:
        ValueError: If any configuration value is invalid or inconsistent.
    """
    validate_required_keys(raw_config)

    width = parse_int(raw_config["width"], "width")
    height = parse_int(raw_config["height"], "height")
    entry = parse_coordinates(raw_config["entry"], "entry")
    exit_point = parse_coordinates(raw_config["exit"], "exit")
    output_file = raw_config["output_file"].strip()
    perfect = parse_bool(raw_config["perfect"], "perfect")

    if width <= 0:
        raise ValueError("WIDTH must be greater than 0")
    if height <= 0:
        raise ValueError("HEIGHT must be greater than 0")
    if not output_file:
        raise ValueError("OUTPUT_FILE must exist")

    validate_bounds(entry, width, height, "ENTRY")
    validate_bounds(exit_point, width, height, "EXIT")

    if entry == exit_point:
        raise ValueError("ENTRY and EXIT must be different")

    config = {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_point,
        "output_file": output_file,
        "perfect": perfect
    }

    if "seed" in raw_config:
        config["seed"] = parse_int(raw_config["seed"], "seed")

    return config


def load_and_parse_config() -> dict:
    """
    Load, parse, and validate the configuration file.

    This is the main helper function for the parser pipeline. It reads the
    config file path from ``sys.argv``, then combines file reading, raw
    parsing, and full validation into one call.

    Returns:
        dict[str, object]: Final validated configuration dictionary.

    Raises:
        ValueError: If the file contents are invalid.
        SystemExit: If the file cannot be opened or CLI arguments are wrong.
    """
    cfg_path = validate_args()
    lines = load_config_file(cfg_path)
    raw_config = parse_config_lines(lines)
    return build_and_validate_config(raw_config)
