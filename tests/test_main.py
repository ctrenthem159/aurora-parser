from ui import cli
import app.db as db, app.export as export

def test_main_runs_successfully(mocker):
    mock_args = mocker.patch("sys.argv", [
        "aurora_parser",
        "tests/sample.db",
        "test_output",
        "--format", "json",
        "--log-level", "INFO"
    ])

    mock_connect = mocker.patch.object(db, "connect_db")
    mock_connect.return_value = "engine"

    mock_get = mocker.patch.object(db, "get_events")
    mock_get.return_value = "raw_df"

    mock_filter = mocker.patch.object(db, "filter_events")
    mock_filter.return_value = "filtered_df"

    mock_export = mocker.patch.object(export, "export_data")

    result = cli.main()

    assert result == 0
    mock_connect.assert_called_once_with("tests/sample.db")
    mock_get.assert_called_once_with("engine")
    mock_filter.assert_called_once_with("engine", "raw_df")
    mock_export.assert_called_once_with("filtered_df", filename="test_output.json", format="json")

def test_main_returns_early_on_db_failure(mocker):
    mocker.patch("sys.argv", ["aurora_parser", "bad.db", "output"])
    mocker.patch.object(db, "connect_db", return_value=None)

    result = cli.main()
    assert result is None  # or whatever is expected when DB fails
