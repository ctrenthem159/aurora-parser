# Aurora Parser

A simple interactive tool to extract your empire's logs from the Aurora database and export them to a variety of formats to use downstream. The tool was originally built to pull game logs as a .csv file to hand off to ChatGPT for creating narratives, but it can be used for a wide variety of uses.

## 🚀 Features

- Interactive menu to select your save and empire. (It will show you all empires, including NPRs and Precursors)
- Export logs to csv, json, excel, human-readable text, and html

## 🛠️ Installation

For now, you have to clone the repo and install the requirements manually. A functional installer is coming later.

```bash
git clone https://github.com/ctrenthem159/aurora-parser
cd aurora-parser
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📦 Usage

```bash
python [--format csv] [--log-level INFO] [--log_file output.log] src/main.py path/to/AuroraDB.db path/to/output.file
```

### Arguments

- `--format`: choose the output file format. Options are csv, json, xlsx (excel spreadsheet), txt (human-readable text file), or html
- `--log-level`: set the logging level. All standard log levels are available
- `--log-file`: output the log to a file. Be sure to include this when opening a support ticket.

All of these arguments are optional. The format defaults to a csv file and logging defaults to `INFO` and logs directly to stdout.

## 🧪 Testing

This project uses pytest for testing, just run `pytest` to run tests.

To run with coverage:

```bash
pytest --cov=src tests/
coverage report
coverage html  # view HTML report in `htmlcov/index.html
```

Currently, tests cover the db functions only but the rest is in progress.

---

## 🔭 Roadmap

- [x] Multi-format export
- [x] Pytest coverage and logging
- [x] GUI interface (PyQt)
- [x] Conversion to a live viewer in addition to exporting logs
- [ ] Viewer for other database areas that users find relevant. (Unless Steve says otherwise, this tool will not allow modifying the database)

## 📄 Legal

PolyForm Noncommercial (full license available in [[LICENSE]])

AI Usage Disclosure is located at [[DISCLOSURE.md]]

## 🧠 Credits

Created and maintained by @ctrenthem159, not yet Steve-approved (but will be once it's ready!)
