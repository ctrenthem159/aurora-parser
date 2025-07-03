import pytest
import pandas as pd
from app import db

@pytest.fixture
def sample_engine():
    return db.connect_db('tests/sample.db')

@pytest.fixture
def sample_df(sample_engine):
    query = "SELECT * FROM FCT_GameLog WHERE RaceID = 588 LIMIT 10"
    with sample_engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

@pytest.fixture
def mock_logger_db(mocker):
    return mocker.patch("app.db.logger")

@pytest.fixture
def mock_logger_export(mocker): 
    return mocker.patch("app.export.logger")

@pytest.fixture
def mock_logger_cli(mocker): 
    return mocker.patch("ui.cli.logger")