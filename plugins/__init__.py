s# plugins package. Import plugin classes here for loader convenience.
from .food import FoodPlugin
from .weather import WeatherPlugin
from .movienight import MovieNightPlugin
from .keyword_response import KeywordResponsePlugin

ALL_PLUGINS = [
    FoodPlugin,
    WeatherPlugin,
    MovieNightPlugin,
    KeywordResponsePlugin,
]
