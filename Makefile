# Config
PYTHON  = python3
MAIN    = a_maze_ing.py
CONFIG  = config.txt

# Install
.PHONY: install
install:
# 	python3 -m venv .amazeing
	pip install -e .
	pip install flake8
	pip install mypy

# Run
.PHONY: run
run:
	$(PYTHON) $(MAIN) $(CONFIG)

# Debug
.PHONY: debug
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# Clean
.PHONY: clean
clean:
	rm -rf __pycache__ */__pycache__ **/__pycache__ .mypy_cache *.pyc

# Lint
.PHONY: lint
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	        --disallow-untyped-defs --check-untyped-defs