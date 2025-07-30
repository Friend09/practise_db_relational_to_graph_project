.PHONY: compile install help

compile:
	uv pip compile -o requirements.txt requirements.in

install:
	uv pip install -r requirements.txt

help:
	@echo "Available commands:"
	@echo "  make compile   - Compile requirements.in to requirements.txt"
	@echo "  make install   - Install dependencies from requirements.txt"
	@echo "  make help      - Show this help message"
