# NBA Stats Fetcher Module

## Overview

The `src/fetch_nba_stats.py` module provides functionality to fetch NBA player game logs using the `nba_api` package. It returns historical game data in a pandas DataFrame with standardized columns.

## Features

- **Player Search**: Find NBA players by full name
- **Game Log Retrieval**: Get historical game statistics for any NBA player
- **Standardized Output**: Returns DataFrame with consistent columns: `date`, `opponent`, `points`, `assists`, `rebounds`, `minutes`
- **Error Handling**: Graceful fallback to mock data when NBA API is unavailable
- **Batch Processing**: Support for fetching data for multiple players
- **Season Selection**: Specify which NBA season to fetch data from

## Installation

The module requires the following dependencies (already included in `requirements.txt`):

```
nba_api
pandas
```

## Usage

### Basic Usage

```python
from src.fetch_nba_stats import get_player_game_logs

# Get game logs for a player
df = get_player_game_logs("LeBron James")
print(df.head())
```

### Specify Season

```python
# Get data for a specific season
df = get_player_game_logs("Stephen Curry", season="2022-23")
```

### Use Mock Data

```python
# Force use of mock data for testing
df = get_player_game_logs("LeBron James", use_mock=True)
```

### Multiple Players

```python
from src.fetch_nba_stats import get_multiple_players_game_logs

players = ["LeBron James", "Stephen Curry", "Giannis Antetokounmpo"]
results = get_multiple_players_game_logs(players)

for player, df in results.items():
    print(f"{player}: {len(df)} games")
```

## Output Format

The function returns a pandas DataFrame with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `date` | string | Game date in YYYY-MM-DD format |
| `opponent` | string | Opponent team abbreviation |
| `points` | int | Points scored by the player |
| `assists` | int | Assists recorded by the player |
| `rebounds` | int | Rebounds recorded by the player |
| `minutes` | float | Minutes played (converted from MM:SS format) |

### Sample Output

```
         date opponent  points  assists  rebounds  minutes
0  2024-01-15      GSW      28        7         8     36.4
1  2024-01-12      BOS      25        9         6     38.2
2  2024-01-10      MIA      32        6        11     40.0
```

## API Functions

### `get_player_game_logs(player_name, season="2023-24", use_mock=False)`

Retrieve game logs for a single player.

**Parameters:**
- `player_name` (str): Full name of the NBA player (e.g., "LeBron James")
- `season` (str): NBA season in "YYYY-YY" format (default: "2023-24")
- `use_mock` (bool): Force use of mock data for testing (default: False)

**Returns:**
- `pandas.DataFrame`: Game logs with columns: date, opponent, points, assists, rebounds, minutes

**Raises:**
- `ValueError`: If player is not found
- `ConnectionError`: If unable to fetch data from NBA API (falls back to mock data)

### `find_player_by_name(player_name)`

Search for an NBA player by full name.

**Parameters:**
- `player_name` (str): Full name of the player

**Returns:**
- `dict` or `None`: Player information dictionary or None if not found

### `get_multiple_players_game_logs(player_names, season="2023-24", use_mock=False)`

Retrieve game logs for multiple players.

**Parameters:**
- `player_names` (List[str]): List of player names
- `season` (str): NBA season in "YYYY-YY" format (default: "2023-24")
- `use_mock` (bool): Force use of mock data for testing (default: False)

**Returns:**
- `Dict[str, pandas.DataFrame]`: Dictionary mapping player names to their game log DataFrames

## Error Handling

The module includes comprehensive error handling:

1. **Player Not Found**: Returns `ValueError` if player name is invalid
2. **Network Issues**: Automatically falls back to mock data if NBA API is unavailable
3. **Data Processing Errors**: Returns empty DataFrame with correct column structure
4. **Logging**: Comprehensive logging for debugging and monitoring

## Testing

Run the test suite to validate functionality:

```bash
python test_nba_stats.py
```

The test suite covers:
- Player search functionality
- Game log retrieval with mock data
- API fallback behavior
- Multiple player support
- Error handling scenarios

## Example Script

See `example_usage.py` for a comprehensive demonstration of the module's capabilities.

## Integration

The module integrates seamlessly with the existing NBA PrizePicks model codebase:
- Follows the same logging patterns
- Uses consistent error handling approaches
- Maintains the same code style and documentation standards
- Compatible with existing pandas-based workflows

## Performance Notes

- Player search is performed locally using `nba_api.stats.static.players` (fast)
- Game log retrieval requires API calls to NBA.com (may be slower)
- Mock data mode provides instant responses for testing
- Results are returned in DataFrame format for easy analysis and manipulation

## Limitations

- Requires internet connection for live NBA API access
- Subject to NBA.com rate limiting and availability
- Historical data availability depends on NBA.com archives
- Player names must match NBA official records exactly