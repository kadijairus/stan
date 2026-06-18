"""Enum for text labels."""

from enum import Enum


class Label(Enum):
    """Configure UI text labels."""

    # Title
    LABEL = "Etikett"
    RESULT = "Tulemus"

    # Variables for label generation
    FIRST_ELEMENT_TO_BARCODE = "Juhtumi number"
    SECOND_ELEMENT_TO_BARCODE = "Tütar"
    THIRD_ELEMENT_TO_BARCODE_RANGE = "Vahemik"
    DATA_TO_LABEL = "Nimi"

    # Buttons and actions
    RUN = "Tee etikette"

    # Error and status messages
    FORWARDING_DATA = "Saadan etiketi generaatorisse teksti: "
    SUCCESS_MESSAGE = "Etiketi genereerimine õnnestus!"
    FAIL_MESSAGE = "Etiketi genereerimine ebaõnnestus."
    ERROR = "Viga"
    ERROR_NO_FIRST_ELEMENT = f"Vigane seadistus: '{FIRST_ELEMENT_TO_BARCODE}' märkimata."
    ERROR_FILE_NOT_FOUND = "Süsteemi viga: ei leitud käivituskäsus nimetatud faili: "
    ERROR_TIMEOUT = "Ühenduse viga: ooteaeg sai täis."
    ERROR_CORE = "Süsteemi viga: "

