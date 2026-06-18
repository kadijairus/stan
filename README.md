# Stan
Stan helps to send your data to stdin and use in headless applications. Currently supports sending data to label generator. For other applications, change the Label texts and script path.

# Generate executable:
uv run python -m PyInstaller --name="Stan" --onefile --paths=src --distpath dist --contents-directory="src" src/gui.py
