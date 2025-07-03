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


def filter_events(engine, df):
    from prompt_toolkit.shortcuts import radiolist_dialog
    query_game = "SELECT GameID, GameName FROM FCT_Game"
    games_df = pd.read_sql_query(query_game, engine)
    game = games_df[["GameID", "GameName"]].values.tolist()
    logger.debug(f'List of available games: {game}')

    selection_game = radiolist_dialog(
        title="Select a Game",
        text="Choose the game your race is in:",
        values=game
    ).run()

    query_race = f"SELECT RaceID, RaceName FROM FCT_Race WHERE GameID = {selection_game}"
    races_df = pd.read_sql_query(query_race, engine)
    races = races_df[["RaceID", "RaceName"]].values.tolist()
    logger.debug(f'List of available races: {races}')

    selection_race = radiolist_dialog(
        title="Select a Race",
        text="Choose which race you want to view events for:",
        values=races
    ).run()

    filtered_df = df[df['RaceID'] == selection_race]
    logger.debug(filtered_df.head())

    return filtered_df