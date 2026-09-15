![](assets/favicon.ico)

# Stan
Stan is a helpful GUI, that sends your data to stdin and starts another script as subprocess. Currently supports sending data to label generator. For other applications, change the Label texts and script path.

# Generate executable:
```uv run python -m PyInstaller --name="Stan-latest" --onefile --console --paths=src --distpath dist --contents-directory="src" --clean --icon="assets/favicon.ico" --add-data "assets;assets" src/gui.py```
