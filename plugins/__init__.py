# plugins package. Import plugin classes here for loader convenience.
from .food import FoodPlugin
from .weather import WeatherPlugin
from .movienight import MovieNightPlugin
from .keyword_response import KeywordResponsePlugin
from .fun_commands import FunCommandsPlugin
from .utility import UtilityPlugin
from .image_commands import ImageCommandsPlugin

ALL_PLUGINS = [
    FoodPlugin,
    WeatherPlugin,
    MovieNightPlugin,
    KeywordResponsePlugin,
    FunCommandsPlugin,
    UtilityPlugin,
    ImageCommandsPlugin,
]
