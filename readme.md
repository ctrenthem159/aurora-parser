# Aurora Parser

![logo](src/assets/logo.ico)

[![codecov](https://codecov.io/gh/ctrenthem159/aurora-parser/graph/badge.svg?token=9CEC8HSTD0)](https://codecov.io/gh/ctrenthem159/aurora-parser)

A simple interactive tool to extract your empire's logs from the Aurora database and export them to a variety of formats to use downstream. The tool was originally built to pull game logs as a .csv file to hand off to ChatGPT for creating narratives, but it can be used for a wide variety of uses.

## 🚀 Features

![main menu screenshot](src/assets/image.png)

- Interactive menu to select your race (or any race you want to view)
- See your gamelogs directly in the app, with readable timestamps
- Export logs to a variety of formats including csv and json

## 🛠️ Installation

You can download the latest release from [the Releases page on GitHub](https://github.com/ctrenthem159/aurora-parser/releases). Currently the app is available for Windows and Linux.

## 📦 Usage

When the app opens, you can select your `AuroraDB` file that contains your current save. Unless the database structure changes, this app should be compatible with most recent versions of Aurora.

Upon selecting a game database, use the dropdowns to choose your savegame and race, then hit "Load".

If you want to export your entire game log, use the "Export" button at the bottom. You can save it in a variety of formats including json, csv, and excel.

## 🧪 Development & Testing

Developers and writers looking to contribute should review the [contribution guidelines](CONTRIBUTING.md).

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
- [x] Self-contained executable file (for distribution)

## 📄 Legal

[PolyForm Noncommercial license](LICENSE)

[AI Usage Disclosure](DISCLOSURE.md)

## 🧠 Credits

Created and maintained by @ctrenthem159
