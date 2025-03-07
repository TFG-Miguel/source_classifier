# URL Verification Tool

## Overview
This project is a URL verification tool that checks web links against predefined rules. It ensures that URLs comply with allowed MIME types, do not belong to forbidden domains, and do not exceed a set limit for specific keyword mentions.

## Project Structure
The project consists of three main components:

- `main.py` - The entry point that loads data, applies verification rules, and writes the results to a CSV file.
- `utils.py` - Utility functions for handling file operations, extracting website data, and managing MIME types.
- `verifier.py` - The core verification logic that processes URLs based on predefined rules.

## How It Works
1. **Load Rules** - The `Verifier` class reads rules from `config/rules.json`.
2. **Load Data** - URLs are loaded from `data/source.json`.
3. **Verify URLs** - Each URL is checked against:
   - Forbidden domains
   - Allowed MIME types
   - Keyword mention limits
4. **Write Results** - The verification results are stored in `data/final_result.csv`.

## Installation & Usage
### Prerequisites
- Python 3.x
- Install dependencies:
  ```sh
  pip install tqdm beautifulsoup4 requests
  ```

### Running the Tool
Execute the `main.py` script:
```sh
python main.py
```

## Configuration
### Rules File ([`config/rules.json`](./config/rules.json))
The verification logic relies on a JSON rules file with the following structure:
```json
{
  "forbidden-domains": {
    "Reason1": ["example.com", "test.com"]
  },
  "allowed-mime-types": ["text/html", "application/pdf"],
  "multiples-mentions": {
    "regex": "angular\\d*js",
    "limit": 3
  }
}
```

### Source Data ([`data/source.json`](./data/source.json))
The URLs to verify are stored in a JSON file in key-value pairs:
```json
{
  "Group1": ["https://example.com", "https://test.com"],
  "Group2": ["https://sample.com"]
}
```

## Output
Results are saved in [`data/result.csv`](./data/result.csv) with the format:
```
Page,Valid,Reason/Notes,Review,Url
Group1,No,FORBIDDEN DOMAIN: example.com,No,https://example.com
Group1,Yes,,No,https://test.com
```