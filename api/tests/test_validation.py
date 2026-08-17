from validation import validate_measurement


def test_valid_measurement():
    data = {
        "deviceId": "sensor-001",
        "temperature": 21.5,
        "humidity": 45.0,
        "battery": 90,
    }
    assert validate_measurement(data) == []


def test_missing_temperature():
    data = {
        "deviceId": "sensor-001",
        "humidity": 45.0,
        "battery": 90,
    }
    assert "temperature is required" in validate_measurement(data)


def test_invalid_temperature_type():
    data = {
        "deviceId": "sensor-003",
        "temperature": "ERROR",
    }
    assert "temperature must be a number" in validate_measurement(data)

# 1
def test_invalid_id():
    data = {
        "deviceId": "sensor",
        "temperature": 21.5,
        "humidity": 45.0,
        "battery": 90,
    }
    assert "deviceId must contain a number" in validate_measurement(data)

# 2 
def test_too_low_temp():
    data = {
        "deviceId": "sensor-001",
        "temperature": -1.0,
        "humidity": 45.,
        "battery": 90,
    }
    assert "temperature must be above 5 and below 125 degrees" in validate_measurement(data)

# 3
def test_too_high_battery():
    data = {
        "deviceId": "sensor-001",
        "temperature": 21.5,
        "humidity": 45.0,
        "battery": 101,
    }
    assert "battery must be between zero and 100" in validate_measurement(data)

# 4
def test_too_low_humidity():
    data = {
        "deviceId": "sensor-001",
        "temperature": 21.5,
        "humidity": 0.0,
        "battery": 90,
    }
    assert "humidity must be above 10 and below 100" in validate_measurement(data)