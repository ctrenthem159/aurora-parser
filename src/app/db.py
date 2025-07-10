from sqlalchemy import create_engine
from datetime import datetime, timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def connect_db(db_file):
    try:
        db_url = f'sqlite:///{db_file}'
        engine = create_engine(db_url)
        return engine
    except:
        logger.error(f"Failed to connect to the database at {db_file}. Please check the file path and ensure the database exists.")
        return None
    
def get_events(engine):
    query = "SELECT * FROM FCT_GameLog"
    df = pd.read_sql_query(query, engine)
    logger.debug(df.head())

    return df

def get_saves(engine):
    query_game = "SELECT GameID, GameName FROM FCT_Game"
    games_df = pd.read_sql_query(query_game, engine)
    game = games_df[["GameID", "GameName"]].values.tolist()
    logger.debug(f'List of available games: {game}')
    return game

def get_races(engine, game_id):
    query_race = f"SELECT RaceID, RaceName FROM FCT_Race WHERE GameID = {game_id}"
    races_df = pd.read_sql_query(query_race, engine)
    races = races_df[["RaceID", "RaceName"]].values.tolist()
    logger.debug(f'List of available races: {races}')
    return races

def filter_events(engine, df, gameID, raceID):
    filtered_df = df[df['RaceID'] == raceID].copy()
    logger.debug(filtered_df.head())

    # Convert event timestamps to real dates
    query = f'SELECT StartYear FROM FCT_Game WHERE GameID = {gameID}'
    start_year = pd.read_sql_query(query, engine).iloc[0, 0]
    start_datestamp = datetime(start_year, 1, 1, 0, 0, 0)

    filtered_df.loc[:, 'Timestamp'] = filtered_df['Time'].apply(lambda sec: start_datestamp + timedelta(seconds=sec))

    return filtered_df