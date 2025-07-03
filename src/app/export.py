import logging

logger = logging.getLogger(__name__)

def export_data(df, filename, format='csv'):
    try:
        format = format.lower()
        if format == 'csv':
            df.to_csv(filename, index=False)
        elif format == 'json':
            df.to_json(filename, orient='records', lines=True)
        elif format == 'xlsx':
            try:
                df.to_excel(filename, index=False)
            except:
                logger.error("Failed to export to Excel. Ensure you have 'openpyxl' or 'xlsxwriter' installed.")
                raise
        elif format == "txt":
            with open(filename, "w", encoding="utf-8") as f:
                f.write(df.to_string(index=False))
        elif format == 'html':
            df.to_html(filename, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        logger.info(f"Data successfully exported to {filename} in {format} format.")
    except Exception as e:
        logger.error(f"Failed to export data to {filename}: {e}")