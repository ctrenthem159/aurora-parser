from app import db
import pandas as pd
from pandas.testing import assert_frame_equal

def test_connect_db(sample_engine):
    # Test the connect_db function to ensure it returns a valid SQLAlchemy engine
    assert sample_engine is not None, "Expected connect_db() to return an engine, got None"
    assert str(sample_engine.url) == "sqlite:///tests/sample.db", f"Unexpected engine URL: {repr(str(sample_engine.url))}, Expected {repr('sqlite:///sample.db')}"

def test_connect_db_fail(mock_logger_db, mocker):
    # Test the connect_db function to ensure it handles connection failures gracefully
    mocker.patch("app.db.create_engine", side_effect=Exception("Connection failed"))
    db_file = './path/to/nonexistent.db'
    engine = db.connect_db(db_file)
    assert engine is None, "Expected connect_db() to return None on failure"

    # Check that the error was logged correctly
    mock_logger_db.error.assert_called_once()
    logged_msg = mock_logger_db.error.call_args[0][0]
    expected_msg = (f'Failed to connect to the database at {db_file}. Please check the file path and ensure the database exists.')
    assert logged_msg == expected_msg, 'Logged message does not match expected message'

def test_get_events(sample_engine, mock_logger_db):
    # Test the get_events function to ensure it retrieves events correctly
    df = db.get_events(sample_engine)
    assert not df.empty, "Expected get_events() to return a non-empty DataFrame"

    expected_columns = {'IncrementID', 'GameID', 'RaceID', 'EventType', 'MessageText'}
    assert expected_columns.issubset(df.columns), "Dataset is missing required columns"

    # Check that the debug log was called with the DataFrame head
    mock_logger_db.debug.assert_called_once()
    try:
        assert_frame_equal(mock_logger_db.debug.call_args[0][0], df.head())
    except AssertionError as e:
        raise AssertionError("Logged DataFrame head does not match expected DataFrame head") from e
    
def test_get_saves(sample_engine, mock_logger_db):
    df = db.get_saves(sample_engine)
    #TODO Test that the list of games from the database matches the expected list
    assert df == [[115, 'Galactic Empire']]
    assert len(df) == 1

    # Check that the debug log was called with the correct output list
    mock_logger_db.debug.assert_called_once()
    assert mock_logger_db.debug.call_args[0][0] == "List of available games: [[115, 'Galactic Empire']]"

def test_get_races(sample_engine, mock_logger_db):
    df = db.get_races(sample_engine, 115)
    #TODO Test that the list of games from the database matches the expected list
    assert df == [[588, 'Terran'], [589, 'Aaanthor'], [590, 'Eldar'], [591, 'Precusors'], [592, 'Invaders'], [593, 'Rhoeng'], [594, 'Alris Corvin'], [595, 'Odzani']]
    assert len(df) == 8

    # Check that the debug log was called with the correct output list
    mock_logger_db.debug.assert_called_once()
    assert mock_logger_db.debug.call_args[0][0] == "List of available races: [[588, 'Terran'], [589, 'Aaanthor'], [590, 'Eldar'], [591, 'Precusors'], [592, 'Invaders'], [593, 'Rhoeng'], [594, 'Alris Corvin'], [595, 'Odzani']]"

def test_filter_events(sample_engine, mock_logger_db, mocker):
    df = pd.read_sql_query("SELECT * FROM FCT_GameLog", sample_engine)

    # Mock the radiolist_dialog to return a specific game
    mock_dialog =  mocker.patch("prompt_toolkit.shortcuts.radiolist_dialog")
    mock_dialog.return_value.run.side_effect = [115, 588]

    filtered_df = db.filter_events(sample_engine, df, gui=False)

    # Validate the filtered DataFrame contains only the events being targetted
    assert not filtered_df.empty, "Expected filter_events() to return a non-empty DataFrame"
    assert all(filtered_df['RaceID'] == 588), "Expected all RaceID in filtered DataFrame to match the sample RaceID (588)"

    # Assert: logger.debug called at least 3 times
    assert mock_logger_db.debug.call_count >= 3

    # Validate the log messages are correct
    debug_calls = [call.args[0] for call in mock_logger_db.debug.call_args_list]
    assert any("List of available games" in msg for msg in debug_calls)
    assert any("List of available races" in msg for msg in debug_calls)