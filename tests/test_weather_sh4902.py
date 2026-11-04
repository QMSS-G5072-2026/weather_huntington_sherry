
"""Tests for the weather_sh4902 package."""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import weather_sh4902
from weather_sh4902 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)


def test_version_is_defined():
    assert isinstance(weather_sh4902.__version__, str)


# PART 1: UNIT TESTS

@pytest.mark.parametrize("celsius, expected", [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6),
    (-273.15, -459.67),
])
def test_celsius_to_fahrenheit(celsius, expected):
    """Test Celsius to Fahrenheit conversion."""
    result = celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize("bad_input, expected_error", [
    ("abc", TypeError),
    (None, TypeError),
    (True, TypeError),
    (-273.16, ValueError),
])
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Test invalid temperatures with expected errors."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Test temperature summary with one missing value."""
    temperatures = [-10.0, float("nan"), 0.0, 10.0]
    result = summarize_temperatures(temperatures)

    assert result["mean"] == 0.0
    assert result["min"] == -10.0
    assert result["max"] == 10.0
    assert result["n_missing"] == 1

def test_summarize_temperatures_all_missing():
    """Test that all missing temperatures raise an error."""
    with pytest.raises(ValueError):
        summarize_temperatures([float("nan"), float("nan")])


# PART 2: FIXTURES

@pytest.fixture
def raw_readings():
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": ["2026-07-02", "2026-07-01", "2026-07-01",
                 "2026-07-02", "2026-07-01"],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """Test the fixture columns, number of rows, and missing values."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1


# PART 3: TESTING DATAFRAMES

def test_clean_readings(raw_readings):
    """Test the data is cleaned and temperatures are converted."""
    expected_df = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    cleaned_df = clean_readings(raw_readings)
    assert_frame_equal(cleaned_df, expected_df)
