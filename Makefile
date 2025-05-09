start:
	uv run python3 -m app.db.database
	uv run flask --app app/exemple --debug run --port 8000
install:
	uv sync