from serial_reader.parser import parse_line


def test_valid_line():
    line = '{"ts":1000,"ph":6.2,"tds":840,"water_temp":22.1,"air_temp":24.5,"humidity":68.2,"water_level_cm":18.4}'
    r = parse_line(line)
    assert r is not None
    assert r.ph == pytest.approx(6.2, abs=0.01)
    assert r.tds == pytest.approx(840, abs=1)


def test_error_values_become_none():
    line = '{"ts":1000,"ph":-1.0,"tds":840,"water_temp":-1.0,"air_temp":24.5,"humidity":68.2,"water_level_cm":18.4}'
    r = parse_line(line)
    assert r is not None
    assert r.ph is None
    assert r.water_temp is None
    assert r.tds == pytest.approx(840, abs=1)


def test_malformed_json():
    assert parse_line("not json") is None
    assert parse_line("") is None
    assert parse_line("{bad}") is None


def test_missing_ts():
    line = '{"ph":6.2,"tds":840}'
    assert parse_line(line) is None


import pytest
