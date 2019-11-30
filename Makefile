.PHONY: help
help:
	@echo "help     Display this message"
	@echo "deps     Download dependencies."
	@echo "style    Style repository."

# Core ]-----------------------------------------------
.PHONY: style
style:
	black .

.PHONY: clean
clean:
	rm -rf data

# Test ]-----------------------------------------------
.PHONY: test
test: test.static

.PHONY: test.static
test.static:
	black --check .
	pylint v0

# Exec ]-----------------------------------------------
.PHONY: run
run: deps test

.PHONY: deps
deps: data/emoji_pages.csv

data/emoji_pages.csv: data
	python v0/fetch_emoji_refs.py data/emoji_pages.csv

data:
	mkdir data
