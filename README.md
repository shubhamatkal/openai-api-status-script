# OpenAI API Status Monitor

A lightweight Python script that monitors OpenAI API service status and alerts when components become non-operational.

## Features

- Prints alerts only when service status degrades
- Fetches incident details for context
- Polls OpenAI status API every 60 seconds
- Handles network errors gracefully
- Minimal resource usage

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

```bash
python monitor.py
```

## Output Format

```
[2025-11-16 14:32:00] Product: OpenAI API - Chat Completions
Status: Degraded performance due to upstream issue
```

## Configuration

Edit the following constants in `monitor.py`:

- `CHECK_INTERVAL`: Seconds between status checks (default: 60)
- `TIMEOUT`: HTTP request timeout in seconds (default: 10)

## License

MIT