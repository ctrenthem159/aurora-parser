import logging

logger = logging.getLogger(__name__)

def export_data(df, filename, format='csv'):
    if df.empty:
        logger.warning("DataFrame is empty. No data to export.")
        return

    format = format.lower()
    if format == 'csv':
        df.to_csv(filename, index=False)
    elif format == 'json':
        df.to_json(filename, orient='records', lines=True)
    elif format == 'xlsx':
        try:
            df.to_excel(filename, index=False)
        except:
            raise IOError("Failed to export to Excel. Ensure you have 'openpyxl' or 'xlsxwriter' installed.")
    elif format == "txt":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(df.to_string(index=False))
    elif format == 'html':
        df.to_html(filename, index=False)
    else:
        raise ValueError(f"Unsupported format: {format}")
    logger.info(f"Data successfully exported to {filename}")