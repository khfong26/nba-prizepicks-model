#!/usr/bin/env python3
"""
Test script for NBA stats fetcher module
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetch_nba_stats import get_player_game_logs, find_player_by_name, get_multiple_players_game_logs


def test_player_search():
    """Test player search functionality"""
    print("Testing player search...")
    
    # Test valid players
    lebron = find_player_by_name("LeBron James")
    assert lebron is not None, "Should find LeBron James"
    assert lebron['full_name'] == "LeBron James", "Should match full name"
    assert 'id' in lebron, "Should have player ID"
    
    curry = find_player_by_name("Stephen Curry")
    assert curry is not None, "Should find Stephen Curry"
    assert curry['full_name'] == "Stephen Curry", "Should match full name"
    
    # Test invalid player
    invalid = find_player_by_name("Invalid Player Name")
    assert invalid is None, "Should return None for invalid player"
    
    print("✅ Player search tests passed")


def test_game_logs_mock():
    """Test game logs with mock data"""
    print("Testing game logs with mock data...")
    
    df = get_player_game_logs("LeBron James", use_mock=True)
    
    # Validate DataFrame structure
    assert isinstance(df, pd.DataFrame), "Should return pandas DataFrame"
    
    expected_columns = ['date', 'opponent', 'points', 'assists', 'rebounds', 'minutes']
    assert list(df.columns) == expected_columns, f"Should have columns: {expected_columns}"
    
    # Validate data types
    assert df['date'].dtype == 'object', "Date should be string/object type"
    assert df['points'].dtype in ['int64', 'int32'], "Points should be integer"
    assert df['assists'].dtype in ['int64', 'int32'], "Assists should be integer"
    assert df['rebounds'].dtype in ['int64', 'int32'], "Rebounds should be integer"
    assert df['minutes'].dtype in ['float64', 'float32'], "Minutes should be float"
    
    # Validate data content
    assert len(df) > 0, "Should have at least one game"
    assert all(df['points'] >= 0), "Points should be non-negative"
    assert all(df['assists'] >= 0), "Assists should be non-negative"
    assert all(df['rebounds'] >= 0), "Rebounds should be non-negative"
    assert all(df['minutes'] >= 0), "Minutes should be non-negative"
    
    # Validate date format
    try:
        pd.to_datetime(df['date'])
    except Exception as e:
        assert False, f"Date format should be valid: {e}"
    
    print("✅ Mock game logs tests passed")


def test_game_logs_api():
    """Test game logs with API (will fallback to mock due to network)"""
    print("Testing game logs with API (fallback to mock expected)...")
    
    df = get_player_game_logs("Stephen Curry", season="2023-24")
    
    # Should still return valid DataFrame structure even with API failure
    assert isinstance(df, pd.DataFrame), "Should return pandas DataFrame"
    
    expected_columns = ['date', 'opponent', 'points', 'assists', 'rebounds', 'minutes']
    assert list(df.columns) == expected_columns, f"Should have columns: {expected_columns}"
    
    print("✅ API game logs tests passed (with fallback)")


def test_multiple_players():
    """Test fetching game logs for multiple players"""
    print("Testing multiple players...")
    
    players = ["LeBron James", "Stephen Curry"]
    results = get_multiple_players_game_logs(players, use_mock=True)
    
    assert isinstance(results, dict), "Should return dictionary"
    assert len(results) == 2, "Should have results for both players"
    
    for player in players:
        assert player in results, f"Should have results for {player}"
        df = results[player]
        assert isinstance(df, pd.DataFrame), f"Should have DataFrame for {player}"
        
        expected_columns = ['date', 'opponent', 'points', 'assists', 'rebounds', 'minutes']
        assert list(df.columns) == expected_columns, f"Should have correct columns for {player}"
    
    print("✅ Multiple players tests passed")


def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test invalid player name
    try:
        df = get_player_game_logs("Invalid Player Name That Does Not Exist")
        # Should either raise ValueError or return empty DataFrame (depending on mock usage)
        if not df.empty:
            # If it doesn't raise an error, it should at least return valid structure
            expected_columns = ['date', 'opponent', 'points', 'assists', 'rebounds', 'minutes']
            assert list(df.columns) == expected_columns
    except ValueError:
        # This is expected for invalid player names when not using mock
        pass
    
    print("✅ Error handling tests passed")


def run_all_tests():
    """Run all tests"""
    print("Running NBA stats fetcher tests...\n")
    
    try:
        test_player_search()
        test_game_logs_mock()
        test_game_logs_api()
        test_multiple_players()
        test_error_handling()
        
        print("\n🎉 All NBA stats fetcher tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)