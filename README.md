# UnifiUtils (Python)

A Python utility library for interacting with Ubiquiti UniFi Controller REST APIs. This library provides a clean abstraction layer for HTTP communication with UniFi network controllers, handling authentication, endpoint management, and JSON request/response processing.

Ported from the [Java UnifiUtils](https://github.com/RogerJoys/UnifiUtils) library.

## Features

- **Enumeration-based API interface** - Type-safe API endpoint definitions with 129 UniFi endpoints
- **Dynamic URL templating** - Automatic placeholder substitution for site, MAC address, and other parameters
- **Flexible HTTP methods** - Support for GET, POST, PUT, DELETE, and HEAD operations
- **Built-in authentication** - API key header management for all requests
- **Native JSON handling** - Returns Python dicts directly
- **Comprehensive logging** - Python `logging` module integration for debugging and traceability

## Requirements

- Python 3.10+
- `requests` library

## Installation

### From PyPI
```bash
pip install unifi-utils-python
```

### From Source
```bash
git clone https://github.com/Joys-Advisory-Partners-Unifi/unifi-utils-python.git
cd unifi-utils-python
pip install -e .
```

### Development

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Initialization

```python
from unifi_utils import UnifiUtils, UnifiAPI

# Initialize with UniFi controller details
unifi = UnifiUtils(
    endpoint="https://your-controller.url",  # Controller endpoint
    api_key="your-api-key",                   # API key
    site="default",                            # Site name
)
```

### Making API Calls

```python
# Simple GET request
status = unifi.make_api_call(UnifiAPI.StatusGet)

# Get all active clients
clients = unifi.make_api_call(UnifiAPI.ActiveClientsGet)

# Get site health
health = unifi.make_api_call(UnifiAPI.HealthGet)

# POST request with JSON body
body = {"username": "admin", "password": "password"}
response = unifi.make_api_call(UnifiAPI.LoginPost, json_body=body)

# Device-specific command with MAC address
device_response = unifi.make_api_call(
    UnifiAPI.DeviceLocateEnablePost,
    mac_address="aa:bb:cc:dd:ee:ff",
)

# Full control with custom endpoint substitutions
from unifi_utils import UnifiEndpointSymbolics

substitutions = {UnifiEndpointSymbolics.ID: "device-id-here"}
update_body = {"name": "New Device Name"}
update_response = unifi.make_api_call(
    UnifiAPI.DeviceUpdatePut,
    json_body=update_body,
    added_substitutions=substitutions,
)
```

## Available API Endpoints

The library provides **129 API endpoints** covering all UniFi Controller functionality:

| Category | Count |
|----------|-------|
| Controller APIs (auth, system) | 9 |
| Health & Status | 5 |
| Events & Alarms | 4 |
| Client Management | 11 |
| VPN | 1 |
| Device Management | 16 |
| Network Configuration | 9 |
| Firewall Configuration | 8 |
| Port Forwarding | 4 |
| WLAN Configuration | 5 |
| Site Settings | 2 |
| DPI & Analytics | 6 |
| RADIUS | 8 |
| Dynamic DNS | 3 |
| Switch Port Profiles | 4 |
| Rogue APs | 2 |
| Hotspot / Vouchers / Guests | 5 |
| Hotspot Operators | 4 |
| User Groups | 4 |
| Media Streaming | 2 |
| Backup Commands | 3 |
| Site Management | 6 |
| Event Management | 1 |
| SDN / Cloud Access | 1 |
| Miscellaneous (Tags, Counters, Dashboard, WLAN Groups) | 7 |

## Project Structure

```
unifi-utils-python/
├── src/
│   └── unifi_utils/
│       ├── __init__.py      # Public exports
│       ├── enums.py         # HTTPCall, UnifiApiClass, UnifiCommandManager, UnifiEndpointSymbolics
│       ├── api.py           # UnifiAPI enum (129 endpoint definitions)
│       └── client.py        # UnifiUtils class (main HTTP client)
├── tests/
│   ├── test_enums.py
│   ├── test_api.py
│   └── test_client.py
├── pyproject.toml
├── LICENSE
└── README.md
```

## Core Classes

### UnifiUtils
The main class for interacting with the UniFi Controller API. Provides a single `make_api_call()` method with optional parameters:
- `api_call` - The `UnifiAPI` enum member to call
- `json_body` - Optional dict for POST/PUT request bodies
- `mac_address` - Optional MAC address for device-specific commands
- `added_substitutions` - Optional dict of `UnifiEndpointSymbolics` to string values for URL placeholders

### UnifiAPI
Enumeration defining all supported API endpoints with their paths, HTTP methods, requirements, and manager types.

### UnifiApiClass
Defines API classification types with their URL prefixes:
- `Controller` - Root level endpoints
- `Site` - Site-specific endpoints (`/api/s/{{site}}`)
- `CallableCommand` - Device command endpoints (`/api/s/{{site}}/cmd/{{manager}}`)

### UnifiCommandManager
Defines manager types for command routing: `evtmgt`, `sitemgr`, `stamgr`, `devmgr`, `backup`, `system`, `stat`.

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## API Documentation

For detailed UniFi Controller API documentation, see:
- [UniFi Controller API Reference](https://ubntwiki.com/products/software/unifi-controller/api)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or pull request.
