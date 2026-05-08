.PHONY: test judge-levels validate list clean

PYTHON ?= python3

test: judge-levels

judge-levels:
	$(PYTHON) src/judge.py level_00 levels/level_00/answer.c
	$(PYTHON) src/judge.py level_01 levels/level_01/answer.c
	$(PYTHON) src/judge.py level_02 levels/level_02/answer.c
	$(PYTHON) src/judge.py level_03 levels/level_03/answer.c
	$(PYTHON) src/judge.py level_04 levels/level_04/answer.c
	$(PYTHON) src/judge.py level_05 levels/level_05/answer.c
	$(PYTHON) src/judge.py level_06 levels/level_06/answer.c
	$(PYTHON) src/judge.py level_07 levels/level_07/answer.c
	$(PYTHON) src/judge.py level_08 levels/level_08/answer.c
	$(PYTHON) src/judge.py level_09 levels/level_09/answer.c
	$(PYTHON) src/judge.py level_10 levels/level_10/answer.c
	$(PYTHON) src/judge.py level_11 levels/level_11/answer.c
	$(PYTHON) src/judge.py level_12 levels/level_12/answer.c
	$(PYTHON) src/judge.py level_13 levels/level_13/answer.c
	$(PYTHON) src/judge.py level_14 levels/level_14/answer.c

list:
	$(PYTHON) -m app.cli list

validate:
	$(PYTHON) -m app.cli __validate_levels

clean:
	find . -name "*.out" -delete
