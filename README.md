# Stan
Stan is a helpful GUI, that sends your data to stdin and starts another script as subprocess. Currently supports sending data to label generator. For other applications, change the Label texts and script path.

# Generate executable:
uv run python -m PyInstaller --noconsole --name="Stan-latest" --onefile --paths=src --distpath dist --contents-directory="src" src/gui.py
In case of problems with Antivirus, remove the flag "--noconsole".
