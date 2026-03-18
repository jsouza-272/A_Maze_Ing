import sys


REQUIRED_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]


# Validar sys.argv para checar se nao tem args extras e pegar o caminho
# do arquivo
def validate_args() -> str:
    if len(sys.argv) != 2:
        print("Error: correct use python3 a_maze_ing.py config.txt")
    cfg_path = sys.argv[1]
    return cfg_path


# Ler as linhas do arquivo e tratar possíveis erros
def load_config_file(cfg_path: str) -> list:
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


# Passar por todas as linhas, ignorar comentários e linhas vazias, verificar
# keys e values e montar o raw_config
def parse_config_lines(lines: list) -> dict:
    raw_config = {}

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        parts = line.split('=')
        if len(parts) != 2:
            raise ValueError(f"Line {line_number}: invalid format")

        key = parts[0].strip()
        value = parts[1].strip()

        if not key:
            raise ValueError(f"Line {line_number}: Empty key")
        if not value:
            raise ValueError(f"Line {line_number}: Empty value")
        if key in raw_config:
            raise ValueError(f"Line {line_number}: Duplicated key {key}")

        raw_config[key] = value
    return raw_config


def validate_required_keys(raw_config: dict):
    for key in REQUIRED_KEYS:
        if key not in raw_config:
            raise ValueError(f"Missing key: {key}")


def parse_int(value, key_name):
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{key_name} must be an valid integer")


def parse_coordinates(value, key_name):
    parts = value.split(',')
    if len(parts) != 2:
        raise ValueError(f"{key_name} must be in format x,y")
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        raise ValueError(f"{key_name} must contain valid integers")
    return (x, y)


def parse_bool(value, key_name):
    try:
        if value == "True":
            return True
        if value == "False":
            return False
    except ValueError:
        raise ValueError(f"{key_name} must be in boolean")


def validate_bounds(point, width, height, key_name):
    x, y = point
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"{key_name} out of limits")


def build_and_validate_config(raw_config):
    validate_required_keys(raw_config)

    width = parse_int(raw_config["WIDTH"], "WIDTH")
    height = parse_int(raw_config["HEIGHT"], "HEIGHT")
    entry = parse_coordinates(raw_config["ENTRY"], "ENTRY")
    exit = parse_coordinates(raw_config["EXIT"], "EXIT")
    output_file = raw_config["OUTPUT_FILE"].strip()
    perfect = parse_bool(raw_config["PERFECT"], "PERFECT")

    if width <= 0:
        raise ValueError("WIDTH must be greater than 0")
    if height <= 0:
        raise ValueError("Height must be greater than 0")
    if not output_file:
        raise ValueError("OUTPUT_FILE must exist")

    validate_bounds(entry, width, height, "ENTRY")
    validate_bounds(exit, width, height, "EXIT")

    if entry == exit:
        raise ValueError("ENTRY and EXIT must be different")

    config = {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry,
        "EXIT": exit,
        "OUTPUT_FILE": output_file,
        "PERFECT": perfect
    }

    if "SEED" in raw_config:
        config["SEED"] = parse_int(raw_config["SEED"], "SEED")

    return config


def load_and_parse_config(cfg_path):
    lines = load_config_file(cfg_path)
    raw_config = parse_config_lines(lines)
    return build_and_validate_config(raw_config)
