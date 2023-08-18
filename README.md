`table2anki` - turn HTML tables into Anki card packages
------------------------------------------------------------

## Quickstart

```bash
$ python cli.py --help

Usage: cli.py [OPTIONS]

  Convert an HTML table to an Anki deck.

Options:
  --html TEXT    The HTML string containing the table.
  --file PATH    Path to an HTML file containing the table.
  --url TEXT     URL to fetch and extract tables from.
  --output TEXT  Name of the output Anki deck file.
  --verbose      Enable verbose logging.
  --help         Show this message and exit.
```


## Introduction

`table2anki` is a tool designed to help Anki users swiftly convert tables from HTML sources into Anki decks. Whether you have a table in an HTML file, a raw HTML string, or a webpage, `table2anki` can process it and generate an Anki package ready for import.

## Example

Say you want to measure the mnemonic major system. You find this table at 
[https://major-system.info/en/](https://major-system.info/en/):


| Digit | Letter         |
|-------|----------------|
| 0     | s, z           |
| 1     | t, d, th       |
| 2     | n              |
| 3     | m              |
| 4     | r              |
| 5     | l              |
| 6     | j, ch, sh      |
| 7     | c, k, g, q, ck |
| 8     | v, f, ph       |
| 9     | p, b           |

`table2anki` lets you take that HTML table, and immediately turn it into an Anki
deck. Using the built-in CLI:

```bash
$ python cli.py --url 'https://major-system.info/en/'
DEBUG    Starting new HTTPS connection (1): major-system.info:443
DEBUG    https://major-system.info:443 "GET /en/ HTTP/1.1" 200 None
INFO     Headers: ['Digit', 'Letter']
INFO     Row 1: ['<span class="major-system-0">0</span>', 's, z']
INFO     Row 2: ['<span class="major-system-1">1</span>', 't, d, th']
INFO     Row 3: ['<span class="major-system-2">2</span>', 'n']
INFO     Row 4: ['<span class="major-system-3">3</span>', 'm']
INFO     Row 5: ['<span class="major-system-4">4</span>', 'r']
INFO     Row 6: ['<span class="major-system-5">5</span>', 'l']
INFO     Row 7: ['<span class="major-system-6">6</span>', 'j, ch, sh']
INFO     Row 8: ['<span class="major-system-7">7</span>', 'c, k, g, q, ck']
INFO     Row 9: ['<span class="major-system-8">8</span>', 'v, f, ph']
INFO     Row 10: ['<span class="major-system-9">9</span>', 'p, b']
INFO     Headers: ['<span class="current">S</span>', 'S = 0', '<span class="major-system-0">0</span>']
INFO     Row 1: ['<span class="done">S</span>', 'Vowel, ignored.', '0']
INFO     Row 2: ['<span class="done">Sa</span>', 't = 1', '0']
INFO     Row 3: ['<span class="done">Sat</span>', 'Vowel, ignored.', '01']
INFO     Row 4: ['<span class="done">Sate</span>', 'll = 5, no double letter', '01']
INFO     Row 5: ['<span class="done">Satell</span>', 'Vowel, ignored.', '015']
INFO     Row 6: ['<span class="done">Satelli</span>', 't = 1', '015']
INFO     Row 7: ['<span class="done">Satellit</span>', 'Vowel, ignored.', '0151']
Anki deck saved to output.apkg.
```

If you import `output.apkg` to Anki, a new deck will appear with two fields,
`Digit` and `Letter`. No other CSS or formatting will be applied, but that's
okay -- the bulk import is the hard part. You can do that yourself, however you wish!

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your_username/table2anki.git
```

2. Navigate to the cloned directory:
```bash
cd table2anki
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Detailed Usage

To use `table2anki`, run the `cli.py` script with the desired options. For example, to convert an HTML file to an Anki deck:

```bash
python cli.py --file path_to_html_file.html
```

Or, to fetch tables from a URL:

```bash
python cli.py --url "https://example.com/table_page"
```

For more detailed usage instructions and options, refer to the Quickstart section or use the `--help` flag.

## Features

- Convert tables from raw HTML strings.
- Process tables from HTML files.
- Fetch and convert tables directly from URLs.
- Verbose logging for detailed insights.
- +Customize output Anki deck filename.+

## Contributing

Contributions are welcome! Please submit pull requests or open issues to discuss potential changes or additions.

## License

This project is licensed under CC0. Do with it what you will!
