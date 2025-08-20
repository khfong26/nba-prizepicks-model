#!/usr/bin/env python3
"""
Simple test script for the PrizePicks scraper
"""

import sys
import os
import pandas as pd
from datetime import date

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scrape_prizepicks import PrizePicksScraper

def test_scraper():
    """Test the scraper functionality"""
    print("Testing PrizePicks NBA scraper...")
    
    scraper = PrizePicksScraper()
    
    # Test getting props
    props = scraper.get_nba_props()
    
    # Validate props structure
    assert len(props) > 0, "Should return at least some props"
    
    for prop in props:
        assert 'player' in prop, "Each prop should have player field"
        assert 'stat_type' in prop, "Each prop should have stat_type field"
        assert 'line_value' in prop, "Each prop should have line_value field"
        assert 'matchup' in prop, "Each prop should have matchup field"
        assert 'date' in prop, "Each prop should have date field"
        
        # Validate data types
        assert isinstance(prop['player'], str), "Player should be string"
        assert isinstance(prop['stat_type'], str), "Stat type should be string"
        assert isinstance(prop['line_value'], (int, float)), "Line value should be numeric"
        assert isinstance(prop['matchup'], str), "Matchup should be string"
        assert isinstance(prop['date'], str), "Date should be string"
    
    print(f"✅ Props validation passed ({len(props)} props)")
    
    # Test CSV saving
    output_file = scraper.save_to_csv(props, output_dir='data')
    
    assert os.path.exists(output_file), "CSV file should be created"
    
    # Validate CSV content
    df = pd.read_csv(output_file)
    
    expected_columns = ['player', 'stat_type', 'line_value', 'matchup', 'date']
    assert list(df.columns) == expected_columns, f"CSV should have columns: {expected_columns}"
    
    assert len(df) == len(props), "CSV should have same number of rows as props"
    
    print(f"✅ CSV validation passed ({output_file})")
    
    # Test full run
    output_file2 = scraper.run()
    assert output_file2, "Run method should return output file path"
    assert os.path.exists(output_file2), "Run method should create CSV file"
    
    print("✅ Full run validation passed")
    
    print("🎉 All tests passed!")
    
    return True

if __name__ == "__main__":
    try:
        test_scraper()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)