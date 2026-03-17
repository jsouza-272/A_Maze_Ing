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


def parse_config_value(key, value):
    pass


def validate_config(config):
    pass
