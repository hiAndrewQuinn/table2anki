import random
from bs4 import BeautifulSoup
import genanki
import logging
import colorlog


# Configure logging
def setup_logging():
    """Set up the logging configuration."""
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    }

    colorlog_format = "%(log_color)s%(levelname)-8s%(reset)s " "%(blue)s%(message)s"

    colorlog.basicConfig(
        level=logging.DEBUG, format=colorlog_format, handlers=[colorlog.StreamHandler()]
    )


setup_logging()
logger = logging.getLogger()  # Get the root logger

# Test logging
logger.debug("This is a debug log.")
logger.info("This is an info log.")
logger.warning("This is a warning log.")


def parse_html_table(html_str):
    """
    Parse HTML table and extract its data as well as headers.

    Parameters:
    - html_str (str): The HTML string containing the table.

    Returns:
    - headers (List[str]): The headers extracted from the table.
    - table_data (List[List[str]]): Extracted data from the table.
    """
    soup = BeautifulSoup(html_str, "html.parser")
    headers = []
    table_data = []

    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        for i, row in enumerate(rows):
            cells = row.find_all(["th", "td"])
            row_data = [cell.get_text(strip=True) for cell in cells]
            if i == 0:  # Assuming the first row contains headers
                headers = row_data
            else:
                table_data.append(row_data)

    # Logging the extracted headers and table data
    logger.info(f"Headers: {headers}")
    for index, row in enumerate(table_data, start=1):
        logger.info(f"Row {index}: {row}")

    return headers, table_data


def create_notes(data, model):
    """
    Create Anki notes from the extracted table data.

    Parameters:
    - data (List[List[str]]): Table data.
    - model (genanki.Model): Anki note model.

    Returns:
    - List[genanki.Note]: List of Anki notes.
    """
    notes = []
    for row in data:
        note = genanki.Note(model=model, fields=row)
        notes.append(note)
    return notes


def generate_anki_model(table_name):
    """
    Generate an Anki model based on the given table name.

    Parameters:
    - table_name (List[str]): List of headers which will be the fields of the Anki model.

    Returns:
    - genanki.Model: Anki model for the given table name.
    """
    return genanki.Model(
        random.randint(1000000, 9999999),
        f"{table_name} Model",
        fields=[{"name": name} for name in table_name],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "<br>".join([f"{{{{{name}}}}}" for name in table_name]),
                "afmt": f'{{{{FrontSide}}}}<hr id="answer">{"".join([f"{{{{{name}}}}}" for name in table_name])}',
            },
        ],
    )


def save_to_anki_deck(tables, output_filename="output.apkg"):
    """
    Save extracted table data to an Anki deck.

    Parameters:
    - tables (List[Tuple[str, List[List[str]]]]): List of tables with name and data.
    - output_filename (str, optional): Name of the output file. Defaults to "output.apkg".

    Returns:
    - None
    """
    deck = genanki.Deck(random.randint(1000000, 9999999), "HTML Table Deck")

    for table_name, table_data in tables:
        model = generate_anki_model(table_name)
        notes = create_notes(table_data, model)
        for note in notes:
            deck.add_note(note)

    package = genanki.Package(deck)
    package.write_to_file(output_filename)

if __name__ == "__main__":
    # Sample tables for demonstration purposes
    table1 = (
        """<table><tr><th>Header 1</th></tr><tr><td>Row 1, Cell 1</td></tr></table>"""
    )
    table2 = """<table><tr><th>Header A</th><th>Header B</th></tr><tr><td>Row 1, Cell A</td><td>Row 1, Cell B</td></tr></table>"""
    table3 = """
<table>
  <tr>
    <th>Header 1</th>
    <th>Header 2</th>
    <th>Header 3</th>
  </tr>
  <tr>
    <td>Row 1, Cell 1</td>
    <td>Row 1, Cell 2</td>
    <td>Row 1, Cell 3</td>
  </tr>
  <tr>
    <td>Row 2, Cell 1</td>
    <td>Row 2, Cell 2</td>
    <td>Row 2, Cell 3</td>
  </tr>
  <tr>
    <td>Row 3, Cell 1</td>
    <td>Row 3, Cell 2</td>
    <td>Row 3, Cell 3</td>
  </tr>
</table>
"""
    table4 = """
    <table>
  <tr>
    <th>Header 1</th>
    <th>Header 2</th>
    <th>Header 3</th>
  </tr>
  <tr>
    <td>Row 1, Cell 1 &#128512;</td>
    <td>Row 1, Cell 2 &amp; Special</td>
    <td>Row 1, Cell 3 ♫ Music ♫</td>
  </tr>
  <tr>
    <td>Row 2, Cell 1 &lt; Less Than</td>
    <td>Row 2, Cell 2 &gt; Greater Than</td>
    <td>Row 2, Cell 3 &copy; Copyright</td>
  </tr>
  <tr>
    <td>Row 3, Cell 1 &quot;Quoted&quot;</td>
    <td>Row 3, Cell 2 &apos;Apostrophe&apos;</td>
    <td>Row 3, Cell 3 &amp; Ampersand</td>
  </tr>
</table>
"""

    table1_headers, table1_data = parse_html_table(table1)
    table2_headers, table2_data = parse_html_table(table2)
    table3_headers, table3_data = parse_html_table(table3)
    table4_headers, table4_data = parse_html_table(table4)

    # No, no, with all four.
    tables = [
        (table1_headers, table1_data),
        (table2_headers, table2_data),
        (table3_headers, table3_data),
        (table4_headers, table4_data),
    ]

    save_to_anki_deck(tables)
