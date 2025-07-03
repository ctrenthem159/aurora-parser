import ui.cli, app.logger

if __name__ == "__main__":
    app.logger.setup_logging()
    ui.cli.main()