# Discord Bot - Modular Architecture

This Discord bot has been refactored from a monolithic structure to a modular plugin-based architecture for better maintainability and extensibility.

## Architecture Overview

The bot now uses a plugin system where each feature is implemented as a separate plugin class. This allows for:
- Easy addition/removal of features
- Better code organization
- Reusable components
- Multiple bot instances with different configurations

## File Structure

```
discord-py-wesuck/
├── bot_core.py              # Multi-bot launcher with plugin system
├── main.py                  # Single-bot launcher (alternative)
├── config.json              # Configuration for multiple bot instances
├── install.sh               # Installation script
├── supervisord_sample.conf  # Supervisor configuration
├── plugins/                 # Plugin directory
│   ├── __init__.py         # Plugin registry
│   ├── base_plugin.py      # Abstract base class for plugins
│   ├── food.py             # Food/nutrition lookup
│   ├── weather.py          # Weather and forecast
│   ├── movienight.py       # Movie night scheduling
│   ├── keyword_response.py # Keyword-based responses
│   ├── fun_commands.py     # Fun commands (clap, spongebob, etc.)
│   ├── utility.py          # Utility commands (ping, ip, repeat)
│   └── image_commands.py   # Image-related commands
├── shared/                  # Shared utilities
│   └── utils.py            # Common utility functions
└── txt/                     # Text files and data
    ├── requirements.txt     # Python dependencies
    ├── botmention.txt       # Bot mention responses
    ├── keyword_response.txt # Keyword response data
    ├── movienight.txt       # Movie night data
    ├── movies.csv           # Movie database
    ├── name.txt             # Name data
    ├── quintet-name.txt     # Quintet-specific names
    └── words.txt            # Word data
```

## Running the Bot

### Option 1: Multi-Bot Mode (Recommended)
```bash
python3 bot_core.py
```
This mode supports multiple bot instances defined in `config.json`.

### Option 2: Single-Bot Mode
```bash
python3 main.py
```
This mode runs a single bot instance using environment variables.

## Configuration

### Environment Variables
Set these environment variables for the bot to function:

```bash
export DISCORD_TOKEN="your_discord_token"
export WEATHER_API_KEY="your_openweather_api_key"
export GOOGLE_API_KEY="your_google_maps_api_key"
export GIPHY_API_KEY="your_giphy_api_key"
export REOURL="your_reo_url"
export REOURL2="your_reo_url2"
```

### Multi-Bot Configuration (config.json)
```json
{
  "crystal": {
    "token": "YOUR_CRYSTAL_TOKEN_HERE",
    "name": "crystal",
    "prefix": "!",
    "server_specific": {
      "display_name_file": "quintet-name.txt"
    }
  },
  "marcus": {
    "token": "YOUR_MARCUS_TOKEN_HERE",
    "name": "marcus",
    "prefix": "!",
    "server_specific": {
      "display_name_file": "name.txt"
    }
  }
}
```

## Plugins

### Available Plugins
1. **FoodPlugin**: UPC code lookup for nutrition information
2. **WeatherPlugin**: Current weather and 3-day forecast
3. **MovieNightPlugin**: Movie night scheduling and management
4. **KeywordResponsePlugin**: Keyword-based automatic responses
5. **FunCommandsPlugin**: Fun text manipulation commands
6. **UtilityPlugin**: Utility commands like ping, ip, repeat
7. **ImageCommandsPlugin**: Image-related commands

### Creating New Plugins
To create a new plugin:

1. Create a new file in the `plugins/` directory
2. Inherit from `BasePlugin`
3. Implement the `setup()` method
4. Add your plugin to `plugins/__init__.py`

Example:
```python
from .base_plugin import BasePlugin

class MyPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name="mycommand")
        async def mycommand(ctx):
            await ctx.send("Hello from my plugin!")
```

## Installation

1. Clone the repository
2. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
3. Set up environment variables
4. Run the bot

## Deployment

Use the provided `supervisord_sample.conf` to run the bot as a service. Update the paths and environment variables as needed for your system.

## Features

The refactored bot maintains all the original functionality:
- Weather lookup and forecasting
- Food nutrition information
- Movie night scheduling
- Fun text commands (clap, spongebob, etc.)
- Utility commands (ping, ip, repeat)
- Image commands (driveway, backyard)
- Keyword-based responses
- Multiple bot instance support

## Benefits of the Refactor

1. **Modularity**: Each feature is self-contained
2. **Maintainability**: Easier to debug and modify individual features
3. **Extensibility**: Simple to add new features
4. **Reusability**: Plugins can be shared between bot instances
5. **Configuration**: Support for multiple bot configurations
6. **Testing**: Individual plugins can be tested in isolation
