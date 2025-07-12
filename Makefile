# === USER PARAMETERS

ifdef OS
   export PYTHON_COMMAND=python
   export UV_INSTALL_CMD=powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   export VENV_BIN=.venv/Scripts
else
   export PYTHON_COMMAND=python3.12
   export UV_INSTALL_CMD=curl -LsSf https://astral.sh/uv/install.sh | sh
   export VENV_BIN=.venv/bin
endif

compile:
	uv pip compile pyproject.toml -o requirements.txt
install:
	uv pip sync requirements.txt

format:
	. $(VENV_BIN)/activate && ruff format $(SRC_DIR)

lint:
	. $(VENV_BIN)/activate && ruff check $(SRC_DIR) --fix
	. $(VENV_BIN)/activate && mypy --ignore-missing-imports --install-types --non-interactive --package $(SRC_DIR)

test:
	. $(VENV_BIN)/activate && pytest --verbose --color=yes --cov=$(SRC_DIR)

all-validation: format lint test

update: compile install