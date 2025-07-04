import argparse
import logging
import app.db as db, app.export as export, app.logger as logger

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
    filtered_df = db.filter_events(engine, df, gui=False)
    export.export_data(filtered_df, filename=file, format=args.format)
    return 0