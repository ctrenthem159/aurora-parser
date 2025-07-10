import argparse
import logging
import app.db as db, app.export as export, app.logger as logger
from prompt_toolkit.shortcuts import radiolist_dialog

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog="aurora_parser",
        description="Extract and filter events from an Aurora 4X game database")
    log_group = parser.add_argument_group("Logging Options")
    parser.add_argument("db_path", help="Path to the AuroraDB.db file")
    parser.add_argument("filename", help="Output filename for the events list (excluding file extension)")
    parser.add_argument("--format", default="csv", choices=["csv", "json", "xlsx", "txt", "html"], help="Choose the output format for the events list (csv [default], json, xlsx, txt, html)")
    log_group.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    log_group.add_argument("--log-file", help="Optional log file to write logs to")
    args = parser.parse_args()

    file = f'{args.filename}.{args.format}'

    # setup logging
    logger.setup_logging(getattr(logging, args.log_level), log_file=args.log_file)

    # Establish database connection & perform main logic
    engine = db.connect_db(args.db_path)
    if engine is None:
        return

    df = db.get_events(engine)

    selection_game = radiolist_dialog(
        title="Select a Game",
        text="Choose the game your race is in:",
        values=db.get_saves(engine)
    ).run()

    selection_race = radiolist_dialog(
        title="Select a Race",
        text="Choose which race you want to view events for:",
        values=db.get_races(engine, selection_game)
    ).run()

    filtered_df = db.filter_events(df, selection_race)
    export.export_data(filtered_df, filename=file, format=args.format)
    return 0