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
.PHONY: analyze
analyze: build/model.pckl
	python v0/analyze.py $<

build/model.pckl:
	python v0/trainer.py $< data/html

.PHONY: run
run: data/page_emojis.json build # test
	python v0/trainer.py $< data/html

.PHONY: deps
deps: data/html_emojis.json

data/html: data/page_emojis.json
	mkdir -p $@
	python v0/fetch_emoji_descriptions.py $< $@

data/page_emojis.json: data
	python v0/fetch_emoji_refs.py $@

data:
	mkdir -p $@

build:
	mkdir -p $@
