import click
import requests
from bs4 import BeautifulSoup
from main import save_to_anki_deck, parse_html_table


@click.command()
@click.option(
    "--html",
    "html_string",
    help="The HTML string containing the table.",
    type=str,
    default=None,
)
@click.option(
    "--file",
    "html_file",
    help="Path to an HTML file containing the table.",
    type=click.Path(exists=True, readable=True),
    default=None,
)
@click.option(
    "--url", "url", help="URL to fetch and extract tables from.", type=str, default=None
)
@click.option(
    "--output",
    "output_filename",
    help="Name of the output Anki deck file.",
    type=str,
    default="output.apkg",
)
@click.option("--verbose", is_flag=True, help="Enable verbose logging.")
def table2anki(html_string, html_file, url, output_filename, verbose):
    """Convert an HTML table to an Anki deck."""

    if html_file:
        with open(html_file, "r") as f:
            html_string = f.read()

    if url:
        response = requests.get(url)
        if response.status_code != 200:
            click.echo(
                f"Failed to fetch content from {url}. Status code: {response.status_code}"
            )
            return
        html_string = response.text

    if not html_string:
        click.echo(
            "Please provide an HTML string, specify an HTML file using the --file option, or provide a URL using the --url option."
        )
        return

    soup = BeautifulSoup(html_string, "html.parser")
    tables = soup.find_all("table")

    for table in tables:
        headers, table_data = parse_html_table(str(table))
        if verbose:
            click.echo(f"Headers: {headers}")
            click.echo(f"Data: {table_data}")

        save_to_anki_deck([(headers, table_data)], output_filename)

    click.echo(f"Anki deck saved to {output_filename}.")


if __name__ == "__main__":
    table2anki()
