# Changelog

Nothing worth saying here. It's a changelog. Honestly, I'm surprised you're reading this.

This changelog adheres to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and the program adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.8.0]

### Changed

- Minor changes to make the program act more like a proper piece of software

## [0.7.0]

### Added

- GUI
- Conversion function to generate timestamps for each log entry

### Changed

- Backend database logic separated out for GUI compatability. Unit tests aren't ready for the changes.

### Fixed

- Unit tests are working again. Coverage isn't 100%, but they work.

## [0.6.0] - 2025-07-03

### Added

- Additional unit testing for other functions

## [0.5.0] - 2025-07-03

Changelog for 0.1-0.4 don't exist, everything is merged into 0.5.

### Added

- Unit test structure
- Working unit tests for the database connections
- Additional CLI menu features to select a game and narrow down the races shown for selection
- CLI menu to select a race, showing all races present in the database
- Ability to connect to Aurora's database using hardcoded table values
- Extract log entries into .csv files
- Project documentation

### Changed

- Refactored all logic into separate modules for future-proofing
- Converted from stdout printing to formal logging
- Expanded export options to include json, xlsx, txt, and html