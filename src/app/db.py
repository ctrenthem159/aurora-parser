from sqlalchemy import create_engine
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
    print(races)
    logger.debug(f'List of available races: {races}')
    return races

def filter_events(df, raceID):

    filtered_df = df[df['RaceID'] == raceID]
    logger.debug(filtered_df.head())

    return filtered_df