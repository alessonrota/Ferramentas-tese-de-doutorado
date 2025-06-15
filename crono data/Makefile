
.PHONY: setup pipeline clean

setup:
	poetry install

pipeline:
	poetry run cronodata fetch brasiliana && \
	poetry run cronodata ocr && \
	poetry run cronodata index && \
	poetry run cronodata classify

clean:
	rm -rf data/interim/* data/processed/*
