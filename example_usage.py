#!/usr/bin/env python3
"""
Example usage of the NBA stats fetcher module
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetch_nba_stats import get_player_game_logs, get_multiple_players_game_logs


def main():
    """Demonstrate NBA stats fetcher usage"""
    print("NBA Stats Fetcher - Example Usage")
    print("=" * 40)
    
    # Example 1: Get game logs for a single player
    print("\n1. Getting game logs for LeBron James (using mock data):")
    print("-" * 50)
    
    try:
        df = get_player_game_logs("LeBron James", use_mock=True)
        print(f"Retrieved {len(df)} games:")
        print(df.to_string(index=False))
        
        # Show some stats
        print(f"\nAverage stats:")
        print(f"Points: {df['points'].mean():.1f}")
        print(f"Assists: {df['assists'].mean():.1f}")
        print(f"Rebounds: {df['rebounds'].mean():.1f}")
        print(f"Minutes: {df['minutes'].mean():.1f}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Get game logs for multiple players
    print("\n\n2. Getting game logs for multiple players (using mock data):")
    print("-" * 60)
    
    try:
        players = ["LeBron James", "Stephen Curry", "Giannis Antetokounmpo"]
        results = get_multiple_players_game_logs(players, use_mock=True)
        
        for player, df in results.items():
            print(f"\n{player} - Last 3 games:")
            print(df.head(3)[['date', 'opponent', 'points', 'assists', 'rebounds']].to_string(index=False))
    
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Show how to use with real API (will fallback to mock due to network)
    print("\n\n3. Attempting to use real NBA API (will fallback to mock):")
    print("-" * 60)
    
    try:
        df = get_player_game_logs("Stephen Curry", season="2023-24")
        print(f"Retrieved {len(df)} games for Stephen Curry")
        print("First 2 games:")
        print(df.head(2).to_string(index=False))
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 40)
    print("Example completed!")


if __name__ == "__main__":
    main()