# NBA PrizePicks Scraper

A Python script that scrapes today's NBA player props from PrizePicks and saves them to a CSV file.

## Features

- Scrapes NBA player props from PrizePicks.com
- Exports data to CSV with columns: player, stat_type, line_value, matchup, date
- Robust error handling and fallback to mock data for testing
- Command-line interface with configurable options
- Comprehensive logging and validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/khfong26/nba-prizepicks-model.git
cd nba-prizepicks-model
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python src/scrape_prizepicks.py
```

This will scrape today's NBA props and save them to `data/nba_props_YYYY-MM-DD.csv`.

### Command-Line Options

```bash
python src/scrape_prizepicks.py [OPTIONS]

Options:
  --output-dir DIR    Directory to save CSV files (default: data)
  --mock             Force use of mock data for testing
  --verbose          Enable debug logging
  --help             Show help message
```

### Examples

```bash
# Save to custom directory
python src/scrape_prizepicks.py --output-dir my_data

# Use mock data for testing
python src/scrape_prizepicks.py --mock

# Enable verbose logging
python src/scrape_prizepicks.py --verbose

# Combine options
python src/scrape_prizepicks.py --output-dir results --mock --verbose
```

## Output Format

The script creates a CSV file with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| player | Player name | "LeBron James" |
| stat_type | Type of statistic | "Points", "Assists", "Rebounds" |
| line_value | The prop line value | 25.5 |
| matchup | Game matchup | "LAL @ GSW" |
| date | Date of the props | "2025-08-20" |

### Sample Output

```csv
player,stat_type,line_value,matchup,date
LeBron James,Points,25.5,LAL @ GSW,2025-08-20
Stephen Curry,Assists,6.5,GSW vs LAL,2025-08-20
Anthony Davis,Rebounds,11.5,LAL @ GSW,2025-08-20
```

## How It Works

1. **API First**: The scraper first attempts to find PrizePicks API endpoints for NBA projections
2. **HTML Fallback**: If APIs are unavailable, it falls back to HTML scraping
3. **Mock Data**: If network access fails, it provides mock data for testing
4. **Data Validation**: All scraped data is validated before saving
5. **CSV Export**: Clean data is exported to a timestamped CSV file

## Testing

Run the test suite to validate functionality:

```bash
python test_scraper.py
```

## Error Handling

The scraper includes comprehensive error handling:

- Network timeout handling
- Invalid data filtering
- Graceful fallback to mock data
- Detailed logging for debugging

## Technical Details

### Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `pandas`: Data manipulation and CSV export
- `python-dateutil`: Date handling

### Scraping Strategy

The scraper uses multiple strategies to gather data:

1. **API Endpoints**: Attempts common API patterns
2. **HTML Parsing**: BeautifulSoup for DOM traversal
3. **User-Agent Rotation**: Mimics browser requests
4. **Rate Limiting**: Respectful scraping practices

### Data Processing

- Validates all required fields are present
- Filters for NBA-only content
- Standardizes team name formats
- Handles various date formats

## Development

### Adding New Features

To extend the scraper:

1. Modify the `PrizePicksScraper` class
2. Add new parsing methods
3. Update tests in `test_scraper.py`
4. Update documentation

### Debugging

Use verbose mode for detailed logging:

```bash
python src/scrape_prizepicks.py --verbose
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Troubleshooting

### Common Issues

**No data scraped**: 
- Check internet connection
- Verify PrizePicks website is accessible
- Use `--mock` flag to test with sample data

**CSV not created**:
- Ensure output directory exists and is writable
- Check file permissions

**Import errors**:
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Getting Help

For issues or questions:
1. Check the logs with `--verbose` flag
2. Run tests with `python test_scraper.py`
3. Open an issue on GitHub with error details