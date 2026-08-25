import os
from decimal import Decimal
import psycopg2
import psycopg2.extras


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "jensen_iot"),
        user=os.getenv("DB_USER", "student"),
        password=os.getenv("DB_PASSWORD", "student"),
    )


def _json_ready(row):
    if row is None:
        return None
    result = dict(row)
    for key in ("temperature", "humidity"):
        if isinstance(result.get(key), Decimal):
            result[key] = float(result[key])
    if result.get("created_at") is not None:
        result["created_at"] = result["created_at"].isoformat()
    return result


def get_devices():
    query = """
        SELECT id, device_id, location, device_type
        FROM devices
        ORDER BY device_id;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return [dict(row) for row in cur.fetchall()]


def get_measurements():
    query = """
        SELECT id, device_id, temperature, humidity, battery, created_at
        FROM measurements
        ORDER BY created_at DESC
        LIMIT 100;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return [_json_ready(row) for row in cur.fetchall()]


def device_exists(device_id):
    # -TODO M1-1:
    # Kontrollera om device_id finns i tabellen devices.
    # Returnera True eller False.
    conn = get_connection()
    cursor = conn.cursor()
    sql_query = "SELECT 1 FROM devices WHERE device_id = %s;"
    cursor.execute(sql_query, (device_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def get_statistics():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql_cnt_device = """
        SELECT COUNT(*) AS device_cnt FROM devices;
    """
    sql_cnt_meas = """
        SELECT COUNT(*) AS meas_cnt FROM measurements;
    """
    sql_avg_temp = """
        SELECT AVG("temperature") AS avg_tmp FROM measurements;
    """
    sql_avg_hum = """
        SELECT AVG("humidity") AS avg_hum FROM measurements;
    """

    sql_highest_avg_temp_sensor = """
        SELECT device_id, AVG(temperature) AS avg_temperature
        FROM measurements
        GROUP BY device_id
        ORDER BY avg_temperature DESC
        LIMIT 1;
    """

    sql_most_active_sensor = """
        SELECT device_id, COUNT(*) AS measurement_count
        FROM measurements
        GROUP BY device_id
        ORDER BY measurement_count DESC
        LIMIT 1;
    """
    cursor.execute(sql_cnt_device)
    cnt_device = cursor.fetchone()

    cursor.execute(sql_cnt_meas)
    cnt_meas = cursor.fetchone()

    cursor.execute(sql_avg_temp)
    avg_tmp = cursor.fetchone()
    
    cursor.execute(sql_avg_hum)
    avg_hum = cursor.fetchone()

    cursor.execute(sql_highest_avg_temp_sensor)
    highest_tmp_sens = cursor.fetchone()

    cursor.execute(sql_most_active_sensor)
    most_act = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return {
        "total_devices": cnt_device["device_cnt"],
        "total_measurements": cnt_meas["meas_cnt"],
        "average_temperature": avg_tmp["avg_tmp"],
        "average_humidity": avg_hum["avg_hum"],
        "highest_average_temp_sensor": highest_tmp_sens["avg_temperature"],
        "most_active_sensor": most_act["device_id"]
    }


def get_latest_measurement(device_id):
    # TODO M1-2:
    # Implementera senaste mätvärdet för en sensor.
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql_squery = """
        SELECT * FROM measurements
        WHERE device_id = %s
        ORDER BY created_at DESC
        LIMIT 1;
    """
    cursor.execute(sql_squery, (device_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return _json_ready(result)
    return None


def get_measurements_for_device(device_id):
    # TODO M1-3:
    # Implementera historik för en sensor.
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql_squery = """
        SELECT * FROM measurements
        WHERE device_id = %s
        ORDER BY created_at DESC;
    """
    cursor.execute(sql_squery, (device_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [_json_ready(row) for row in result]


def insert_measurement(data):
    # -TODO M1-4:
    # Spara ett validerat mätvärde i PostgreSQL.
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql_query = """
        INSERT INTO measurements (device_id, temperature, humidity, battery) 
        VALUES (%s, %s, %s, %s) 
        RETURNING *;
    """

    device_id = data.get("deviceId")
    temp = data.get("temperature")
    hum = data.get("humidity")
    batt = data.get("battery")

    cursor.execute(sql_query, (device_id, temp, hum, batt))
    new_row = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return _json_ready(new_row)
