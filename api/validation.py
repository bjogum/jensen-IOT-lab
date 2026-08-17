def validate_measurement(data):
    errors = []

    # -- ID --
    if not data.get("deviceId"):
        errors.append("deviceId is required")
    # 1. Add 'num check' for deviceId
    elif not set("0123456789") & set(data["deviceId"]):
        errors.append("deviceId must contain a number")

    # -- TEMP --
    if "temperature" not in data:
        errors.append("temperature is required")
    elif not isinstance(data["temperature"], (int, float)):
        errors.append("temperature must be a number")
    # 2. Add temp check
    elif not 5 < data["temperature"] < 125:
        errors.append("temperature must be above 5 and below 125 degrees")

    # -- HUMID --
    if "humidity" in data:
        if not isinstance(data["humidity"], (int, float)):
            errors.append("humidity must be a number")
    # 3. Add humid check
        elif not 10 < data["humidity"] < 100:
            errors.append("humidity must be above 10 and below 100")

    # -- BATT --
    if "battery" in data:
        if not isinstance(data["battery"], int):
            errors.append("battery must be an integer")
    # 4. Add battery check 
        elif not 0 <= data["battery"] <= 100:
            errors.append("battery must be between zero and 100")

    return errors
