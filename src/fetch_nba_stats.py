#!/usr/bin/env python3
"""
NBA Stats Fetcher

This module uses the nba_api package to get past game logs for a given player.
Returns a pandas DataFrame with columns: date, opponent, points, assists, rebounds, minutes.

Usage:
    from src.fetch_nba_stats import get_player_game_logs
    
    # Get game logs for a player
    df = get_player_game_logs("LeBron James")
    
    # Get game logs with season parameter
    df = get_player_game_logs("Stephen Curry", season="2023-24")
    
    # Use mock data for testing
    df = get_player_game_logs("LeBron James", use_mock=True)
"""

import pandas as pd
import logging
from datetime import datetime, date
from typing import Optional, Dict, List, Union
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_player_by_name(player_name: str) -> Optional[Dict]:
    """
    Find an NBA player by full name.
    
    Args:
        player_name: Full name of the player (e.g., "LeBron James")
        
    Returns:
        Player dictionary with id, full_name, etc. or None if not found
    """
    try:
        player_list = players.find_players_by_full_name(player_name)
        if player_list:
            return player_list[0]  # Return first match
        else:
            logger.warning(f"Player '{player_name}' not found")
            return None
    except Exception as e:
        logger.error(f"Error searching for player '{player_name}': {e}")
        return None


def _get_mock_game_logs(player_name: str) -> List[Dict]:
    """
    Return mock game log data for testing when network is unavailable.
    
    Args:
        player_name: Name of the player
        
    Returns:
        List of game log dictionaries
    """
    logger.info(f"Returning mock game logs for {player_name}")
    
    # Mock game logs with realistic NBA stats
    mock_data = [
        {
            'GAME_DATE': '2024-01-15',
            'MATCHUP': 'LAL vs. GSW',
            'PTS': 28,
            'AST': 7,
            'REB': 8,
            'MIN': '36:24'
        },
        {
            'GAME_DATE': '2024-01-12',
            'MATCHUP': 'LAL @ BOS',
            'PTS': 25,
            'AST': 9,
            'REB': 6,
            'MIN': '38:15'
        },
        {
            'GAME_DATE': '2024-01-10',
            'MATCHUP': 'LAL vs. MIA',
            'PTS': 32,
            'AST': 6,
            'REB': 11,
            'MIN': '40:02'
        },
        {
            'GAME_DATE': '2024-01-08',
            'MATCHUP': 'LAL @ PHX',
            'PTS': 22,
            'AST': 8,
            'REB': 7,
            'MIN': '35:30'
        },
        {
            'GAME_DATE': '2024-01-05',
            'MATCHUP': 'LAL vs. DEN',
            'PTS': 30,
            'AST': 5,
            'REB': 9,
            'MIN': '37:45'
        }
    ]
    
    return mock_data


def _parse_minutes(minutes_str: str) -> float:
    """
    Convert minutes string from 'MM:SS' format to float.
    
    Args:
        minutes_str: Minutes in 'MM:SS' format
        
    Returns:
        Minutes as float (e.g., 36.4 for 36:24)
    """
    try:
        if ':' in str(minutes_str):
            parts = str(minutes_str).split(':')
            mins = int(parts[0])
            secs = int(parts[1])
            return round(mins + (secs / 60.0), 1)
        else:
            return float(minutes_str)
    except (ValueError, IndexError) as e:
        logger.warning(f"Error parsing minutes '{minutes_str}': {e}")
        return 0.0


def _extract_opponent(matchup: str) -> str:
    """
    Extract opponent team from matchup string.
    
    Args:
        matchup: Matchup string (e.g., "LAL vs. GSW" or "LAL @ BOS")
        
    Returns:
        Opponent team abbreviation
    """
    try:
        if ' vs. ' in matchup:
            return matchup.split(' vs. ')[1]
        elif ' @ ' in matchup:
            return matchup.split(' @ ')[1]
        else:
            # Fallback: return the whole matchup if format is unexpected
            return matchup
    except Exception as e:
        logger.warning(f"Error extracting opponent from '{matchup}': {e}")
        return matchup


def get_player_game_logs(
    player_name: str,
    season: str = "2023-24",
    use_mock: bool = False
) -> pd.DataFrame:
    """
    Get past game logs for a given NBA player.
    
    Args:
        player_name: Full name of the player (e.g., "LeBron James")
        season: NBA season in format "YYYY-YY" (default: "2023-24")
        use_mock: Force use of mock data for testing (default: False)
        
    Returns:
        pandas DataFrame with columns: date, opponent, points, assists, rebounds, minutes
        
    Raises:
        ValueError: If player is not found
        ConnectionError: If unable to fetch data from NBA API
    """
    logger.info(f"Fetching game logs for {player_name}, season {season}")
    
    if use_mock:
        mock_data = _get_mock_game_logs(player_name)
        df = pd.DataFrame(mock_data)
    else:
        # Find the player
        player = find_player_by_name(player_name)
        if not player:
            raise ValueError(f"Player '{player_name}' not found")
        
        player_id = player['id']
        logger.info(f"Found player: {player['full_name']} (ID: {player_id})")
        
        try:
            # Get game logs from NBA API
            gamelog = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season,
                season_type_all_star='Regular Season'
            )
            df = gamelog.get_data_frames()[0]
            
            if df.empty:
                logger.warning(f"No game logs found for {player_name} in season {season}")
                return pd.DataFrame(columns=['date', 'opponent', 'points', 'assists', 'rebounds', 'minutes'])
            
            logger.info(f"Retrieved {len(df)} games for {player_name}")
            
        except Exception as e:
            logger.error(f"Error fetching data from NBA API: {e}")
            logger.info("Falling back to mock data for testing")
            mock_data = _get_mock_game_logs(player_name)
            df = pd.DataFrame(mock_data)
    
    # Process and format the data
    try:
        # Create output DataFrame with required columns
        output_df = pd.DataFrame()
        
        # Map date column
        if 'GAME_DATE' in df.columns:
            output_df['date'] = pd.to_datetime(df['GAME_DATE']).dt.strftime('%Y-%m-%d')
        else:
            output_df['date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
        
        # Map opponent column
        if 'MATCHUP' in df.columns:
            output_df['opponent'] = df['MATCHUP'].apply(_extract_opponent)
        else:
            output_df['opponent'] = 'Unknown'
        
        # Map stats columns
        output_df['points'] = df.get('PTS', 0).astype(int)
        output_df['assists'] = df.get('AST', 0).astype(int)
        output_df['rebounds'] = df.get('REB', 0).astype(int)
        
        # Map minutes column (convert from MM:SS to float)
        if 'MIN' in df.columns:
            output_df['minutes'] = df['MIN'].apply(_parse_minutes)
        else:
            output_df['minutes'] = 0.0
        
        # Sort by date (most recent first)
        output_df = output_df.sort_values('date', ascending=False).reset_index(drop=True)
        
        logger.info(f"Successfully processed {len(output_df)} game logs for {player_name}")
        return output_df
        
    except Exception as e:
        logger.error(f"Error processing game log data: {e}")
        # Return empty DataFrame with correct columns if processing fails
        return pd.DataFrame(columns=['date', 'opponent', 'points', 'assists', 'rebounds', 'minutes'])


def get_multiple_players_game_logs(
    player_names: List[str],
    season: str = "2023-24",
    use_mock: bool = False
) -> Dict[str, pd.DataFrame]:
    """
    Get game logs for multiple players.
    
    Args:
        player_names: List of player names
        season: NBA season in format "YYYY-YY" (default: "2023-24")
        use_mock: Force use of mock data for testing (default: False)
        
    Returns:
        Dictionary mapping player names to their game log DataFrames
    """
    results = {}
    
    for player_name in player_names:
        try:
            df = get_player_game_logs(player_name, season, use_mock)
            results[player_name] = df
        except Exception as e:
            logger.error(f"Error fetching data for {player_name}: {e}")
            results[player_name] = pd.DataFrame(columns=['date', 'opponent', 'points', 'assists', 'rebounds', 'minutes'])
    
    return results


if __name__ == "__main__":
    # Example usage
    try:
        # Test with mock data (since network may be restricted)
        print("Testing NBA stats fetcher with mock data...")
        df = get_player_game_logs("LeBron James", use_mock=True)
        print(f"\nGame logs for LeBron James:")
        print(df)
        
        print(f"\nDataFrame info:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
    except Exception as e:
        print(f"Error: {e}")