from sqlalchemy import create_engine
from datetime import datetime, timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)


# Establish database connection & filters
def connect_db(db_file):
    try:
        db_url = f'sqlite:///{db_file}'
        engine = create_engine(db_url)
        return engine
    except:
        logger.error(f"Failed to connect to the database at {db_file}. Please check the file path and ensure the database exists.")
        return None

def get_saves(engine):
    query_game = "SELECT GameID, GameName FROM FCT_Game"
    games_df = pd.read_sql_query(query_game, engine)
    game = games_df[["GameID", "GameName"]].values.tolist()
    logger.debug(f'List of available games: {game}')
    return game

def get_races(engine, game_id: int, filter: bool):
    # filter NPR races when the filter option is toggled. Otherwise, show all races
    if filter:
        query_race = f"SELECT RaceID, RaceTitle FROM FCT_Race WHERE GameID = {game_id} AND NPR = 0"
    else:
        query_race = f"SELECT RaceID, RaceTitle FROM FCT_Race WHERE GameID = {game_id}"

    races_df = pd.read_sql_query(query_race, engine)
    races = races_df[["RaceID", "RaceTitle"]].values.tolist()
    logger.debug(f'List of available races: {races}')
    return races

# Events Database Tables
def get_events(engine, gameID, raceID):
    query = f'SELECT * FROM FCT_GameLog WHERE RaceID = {raceID}'
    df = pd.read_sql_query(query, engine)
    logger.debug(df.head())

    # Convert event timestamps to real dates
    query = f'SELECT StartYear FROM FCT_Game WHERE GameID = {gameID}'
    start_year = pd.read_sql_query(query, engine).iloc[0, 0]
    start_datestamp = datetime(start_year, 1, 1, 0, 0, 0)

    df.loc[:, 'Timestamp'] = df['Time'].apply(lambda sec: start_datestamp + timedelta(seconds=sec))

    # Convert event type codes to real types
    df_events = pd.read_sql_query('Select * FROM DIM_EventType', engine)
    df['EventType'] = df['EventType'].map(df_events.set_index('EventTypeID')['Description'])

    return df

# Commanders database table
def get_commanders(engine, gameID, raceID):
    query = f"SELECT * FROM FCT_Commander WHERE RaceID = {raceID} AND Deceased = 0"
    df_staff = pd.read_sql_query(query, engine)

    # Convert rank id to names
    df_ranks = pd.read_sql_query(f'SELECT * FROM FCT_Ranks WHERE RaceID = {raceID}', engine)
    df = pd.merge(df_staff, df_ranks, left_on='RankID', right_on='RankID', how='left')

    # Convert system body ids to planet names
    df_planets = pd.read_sql_query(f'SELECT SystemBodyID, Name FROM FCT_SystemBodyName WHERE RaceID = {raceID}', engine)
    df['Homeworld'] = df['HomeworldID'].map(df_planets.set_index('SystemBodyID')['Name'])

    # Classify commanders by their types
    commanderTypes = {0:'Naval', 1:'Ground', 2:'Scientist', 3:'Administrator'}
    df['CommanderType'] = df['CommanderType'].map(commanderTypes)

    # Sort by type, then rank priority, then seniority
    df.sort_values(by=['CommanderType', 'Priority', 'Seniority'], ascending=[True, True, True], inplace=True)

    logger.debug(df.head())
    return df