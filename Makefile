VENV=venv/linux
PYTHON_PACKAGE=pylint_cov


$(VENV):
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e .

venv: $(VENV)

clean:
	rm -rf venv build dist *.egg-info .mypy_cache
	py3clean . -v

install:
	python3 setup.py install --user

test: venv
	$(VENV)/bin/pip install pytest
	$(VENV)/bin/pytest -svvv tests
