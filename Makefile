start:
	# uv run python3 -m app.db.database
	uv run gunicorn --workers=4 --bind=127.0.0.1:8000 app.exemple:app

install:
	uv sync

build_db:
	psql -d $DATABESE_URL