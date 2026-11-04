# read version from installed package
from importlib.metadata import version
__version__ = version("weather_sh4902")
from .weather_sh4902 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)