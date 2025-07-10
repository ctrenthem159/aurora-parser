# Aurora Parser

A simple interactive tool to extract your empire's logs from the Aurora database and export them to a variety of formats to use downstream. The tool was originally built to pull game logs as a .csv file to hand off to ChatGPT for creating narratives, but it can be used for a wide variety of uses.

## 🚀 Features

- Interactive menu to select your race (or any race you want to view)
- See your gamelogs directly in the app, with readable timestamps
- Export logs to a variety of formats including csv and json

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

At present, using the app is no different from development. A functional GUI is ready, but not easy to access yet.

## 🧪 Testing

This project uses pytest for testing, just run `pytest` to run tests.

To run with coverage:

```bash
pytest --cov=src tests/
coverage report
coverage html  # view HTML report in `htmlcov/index.html
```

---

## 🔭 Roadmap

- [x] Multi-format export
- [x] Pytest coverage and logging
- [x] GUI interface (PyQt)
- [x] Conversion to a live viewer in addition to exporting logs
- [ ] Viewer for other database areas that users find relevant. (Unless Steve says otherwise, this tool will not allow modifying the database)
- [ ] Filters to hide NPRs and Precursor races (no spoiler mode)
- [ ] Mapping event types to textual types (Right now, event types show up as numbers, just like in the database itself)
- [ ] Re-write the CLI to match the functionality of the GUI, and make it more suitable for testing/automation
- [ ] Documentation
- [ ] Return to 100% test coverage
- [ ] Self-contained executable file (for distribution)

## 📄 Legal

PolyForm Noncommercial

AI Usage Disclosure is located at in the disclosure document

not yet Steve-approved (but will be once it's ready!)

## 🧠 Credits

Created and maintained by @ctrenthem159
