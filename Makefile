.PHONY: test judge-linear judge-max judge-binary clean

PYTHON ?= python3

test: judge-linear judge-max judge-binary

judge-linear:
	$(PYTHON) src/judge.py linear_search submissions/linear_search.c

judge-max:
	$(PYTHON) src/judge.py max_value submissions/max_value.c

judge-binary:
	$(PYTHON) src/judge.py binary_search submissions/binary_search.c

clean:
	find . -name "*.out" -delete
