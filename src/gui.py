import tkinter as tk
import subprocess
import threading
from importlib import metadata
from enum import Enum

from label import Label

try:
    # Resolves versioning from project specification metadata
    __version__ = metadata.version("stan")
except metadata.PackageNotFoundError:
    __version__ = "1.0.0"

# Define how to call your existing CLI tool.
# During dev, this might be ["uv", "run", "run.py"].
# In production, this will just be ["label_generator.exe"].
CLI_COMMAND = ["uv", "run", "./dist/Labelgenerator.exe"]


class Color(Enum):
    """System color configurations matching framework standards."""
    RED = "#EF416E"
    GREEN = "#00CFB3"
    GRAY_BG = "#F0F0F0"
    TEXT_MAIN = "#000000"
    BLUE = "#12206F"


class HiddenFrame(tk.LabelFrame):
    """Status display frame that stays completely invisible until populated."""

    def __init__(self, master_frame, title) -> None:
        super().__init__(
            master_frame,
            text=title,
            padx=10,
            pady=10,
            font=("Verdana", 10, "bold"),
            fg=Color.BLUE.value,
        )
        self.lbl_log = tk.Label(self, justify="left", anchor="w", wraplength=450)
        self.lbl_log.pack(fill="x", expand=True)

    def update_status(self, message: str, color=Color.TEXT_MAIN.value) -> None:
        """Dynamically toggles visibility based on whether text is provided."""
        if not message:
            self.lbl_log.config(text="")
            self.pack_forget()  # Hides component completely
        else:
            self.lbl_log.config(text=message, fg=color)
            self.pack(fill="x", padx=10, pady=10)  # Reveals component dynamically


class App:
    """Standalone manual interface layer for the execution system."""

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.option_add("*Font", ("Verdana", 10))
        self.window.title(f"Stan v{__version__}")
        self.window.minsize(520, 320)

        # Main window frame anchor
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        # Surrounded Line Container for Label parameters
        self.label_parts_frame = tk.LabelFrame(
            self.main_frame,
            text=Label.LABEL.value,
            padx=15,
            pady=10,
            font=("Verdana", 10, "bold"),
            fg=Color.BLUE.value,
        )
        self.label_parts_frame.pack(fill="x", padx=10, pady=10)
        self.label_parts_frame.columnconfigure(1, weight=1)

        # Inputs with Grid layout inside the boundary frame
        tk.Label(self.label_parts_frame, text=f"{Label.FIRST_ELEMENT_TO_BARCODE.value}:", font=("Verdana", 10, "bold")).grid(row=0, column=0,
                                                                                                     sticky="w", pady=6)
        self.ent_proov = tk.Entry(self.label_parts_frame)
        self.ent_proov.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=6)

        tk.Label(self.label_parts_frame, text=f"{Label.SECOND_ELEMENT_TO_BARCODE.value}:", font=("Verdana", 10, "bold")).grid(row=1, column=0,
                                                                                                     sticky="w", pady=6)
        self.ent_tutar = tk.Entry(self.label_parts_frame)
        self.ent_tutar.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=6)

        tk.Label(self.label_parts_frame, text=f"{Label.THIRD_ELEMENT_TO_BARCODE_RANGE.value}:", font=("Verdana", 10, "bold")).grid(row=2, column=0,
                                                                                                     sticky="w", pady=6)
        self.ent_vahemik = tk.Entry(self.label_parts_frame)
        self.ent_vahemik.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=6)

        tk.Label(self.label_parts_frame, text=f"{Label.DATA_TO_LABEL.value}:", font=("Verdana", 10, "bold")).grid(row=3, column=0,
                                                                                                 sticky="w", pady=6)
        self.ent_nimi = tk.Entry(self.label_parts_frame)
        self.ent_nimi.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=6)

        # Pre-filling field parameters with default values
        self._prefill_fields()

        # Action Trigger Control Panel
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)

        self.btn_print = tk.Button(
            self.button_frame,
            text=Label.RUN.value,
            command=self.start_printing,
            height=2,
            width=22,
            bg=Color.GREEN.value,
        )
        self.btn_print.pack(padx=5)

        # 🙈 Hidden Response Frame (Stays packed away until execution triggers status)
        self.status_frame = HiddenFrame(self.main_frame, Label.RESULT.value)

    def _prefill_fields(self) -> None:
        """Injects default state values into inputs."""
        self.ent_proov.insert(0, "V26001")
        self.ent_tutar.insert(0, "M1")
        self.ent_vahemik.insert(0, "1-3")
        self.ent_nimi.insert(0, "Tamm")

    def start_printing(self) -> None:
        """Pre-processes input variables and dispatches execution sub-thread."""

        # Inline serialization helper to cleanse data fields
        def clean(val: str) -> str:
            return val.replace(".", "").replace(",", "").strip()

        proov = clean(self.ent_proov.get())
        tutar = clean(self.ent_tutar.get())
        vahemik = clean(self.ent_vahemik.get())
        nimi = clean(self.ent_nimi.get())

        if not proov:
            self.status_frame.update_status(f"⚠️ {Label.ERROR_NO_FIRST_ELEMENT.value}", Color.RED.value)
            return

        # Compiles down into clean comma-delimited stream format
        payload = f"{proov},{tutar},{vahemik},{nimi}"

        self.status_frame.update_status(f"{Label.FORWARDING_DATA.value}'{payload}'.", Color.TEXT_MAIN.value)
        self.btn_print.config(state="disabled")

        # Dispatches process on a detached daemon thread to safeguard layout responsiveness
        threading.Thread(target=self._execute_pipeline, args=(payload,), daemon=True).start()

    def _execute_pipeline(self, payload: str) -> None:
        """Communicates payload streaming down into system runtime loop."""
        try:
            result = subprocess.run(
                CLI_COMMAND,
                input=payload,
                capture_output=True,
                text=True,
                timeout=45
            )

            if result.returncode == 0:
                success_msg = result.stdout.strip().splitlines()[-1] if result.stdout else Label.SUCCESS_MESSAGE.value
                # Target window thread for interface mutation safety
                self.window.after(0, lambda: self.status_frame.update_status(f"✅ {success_msg}", Color.GREEN.value))
            else:
                error_trace = result.stderr.strip() or Label.FAIL_MESSAGE.value
                self.window.after(0, lambda: self.status_frame.update_status(f"❌ {Label.ERROR.value}:\n{error_trace}",
                                                                             Color.RED.value))

        except FileNotFoundError:
            self.window.after(0, lambda: self.status_frame.update_status(
                f"❌ {Label.ERROR_FILE_NOT_FOUND.value()}'{CLI_COMMAND}'.", Color.RED.value))
        except subprocess.TimeoutExpired:
            self.window.after(0, lambda: self.status_frame.update_status(
                f"❌ {Label.ERROR_TIMEOUT.value()}", Color.RED.value))
        except Exception as e:
            self.window.after(0, lambda: self.status_frame.update_status(f"❌ {Label.ERROR_CORE.value()}{e}", Color.RED.value))
        finally:
            self.window.after(0, lambda: self.btn_print.config(state="normal"))

    def run(self) -> None:
        """Starts core interface lifecycle loop."""
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()