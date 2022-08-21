.PHONY: all setup clean install

all: setup clean

setup:
	@pip freeze > requirements.txt
	@pip install -r requirements.txt

clean: requirements.txt
	@rm requirements.txt
