"""Test the url generator."""

from unittest.mock import Mock

from providers.tradingeconomics.openbb_tradingeconomics.utils.url_generator import (
    check_args,
    generate_url,
)


def test_check_args_valid():
    query_args = {"country": "US", "start_date": "2023-01-01", "end_date": "2023-01-31"}
    to_include = ["country", "start_date", "end_date"]
    assert check_args(query_args, to_include)


def test_check_args_invalid():
    query_args = {"country": "US"}
    to_include = ["start_date", "end_date"]
    assert not check_args(query_args, to_include)


def create_query_mock(query_dict):
    query_mock = Mock()
    query_mock.dict.return_value = query_dict
    return query_mock


def test_generate_url_country_only():
    query_mock = create_query_mock({"country": "US"})
    expected_url = "https://api.tradingeconomics.com/calendar/country/US?c="
    assert generate_url(query_mock) == expected_url


def test_generate_url_country_and_dates():
    query_mock = create_query_mock(
        {"country": "US", "start_date": "2023-01-01", "end_date": "2023-01-31"}
    )
    expected_url = (
        "https://api.tradingeconomics.com/calendar/country/US/2023-01-01/2023-01-31?c="
    )
    assert generate_url(query_mock) == expected_url


def test_generate_url_importance_only():
    query_mock = create_query_mock({"importance": "High"})
    expected_url = "https://api.tradingeconomics.com/calendar?importance=High&c="
    assert generate_url(query_mock) == expected_url


def test_generate_url_no_data():
    query_mock = create_query_mock({})
    expected_url = "https://api.tradingeconomics.com/calendar?c="
    assert generate_url(query_mock) == expected_url


def test_generate_url_group_only():
    query_mock = create_query_mock({"group": "G20"})
    expected_url = "https://api.tradingeconomics.com/calendar/group/G20?c="
    assert generate_url(query_mock) == expected_url


def test_generate_url_country_group_and_dates():
    query_mock = create_query_mock(
        {
            "country": "US",
            "group": "G20",
            "start_date": "2023-01-01",
            "end_date": "2023-01-31",
        }
    )
    expected_url = "https://api.tradingeconomics.com/calendar/country/US/group/G20/2023-01-01/2023-01-31?c="
    assert generate_url(query_mock) == expected_url