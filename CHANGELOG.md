# Discord Wordy Bot Changelog

All notable changes to this project will be documented in this file.

## Version [1.0.0] - 2022-02-01

- Initial release using Notion as a backend for the bot

## Version [2.0.0] - 2022-02-02

### Added

- Added color blind mode as a toggle when using `/colorblind`
- Added language statistics to the `/stats` command
- Added command `/show` to show your current game
- Added Discord status for bot on start

### Changed

- Changed database from Notion to a local json file
- Changed dependencies - removed `notion-client` and added `pydantic`

