import random
from datetime import datetime, timedelta

def generate_fake_signals(count: int = 100):
    """
    Generate simulated RF signal detections for testing and development.

    Args:
        count (int): Number of dummy RF signal detections to generate.

    Returns:
        list[dict]: A list of JSON-serializable dictionaries containing
        simulated RF signal metadata such as frequency, location,
        power level, modulation type, and anomaly status.
    """
    base_lat = 21.48
    base_lon = -157.98

    emitter_types = ["Radar", "Comms", "WiFi", "Unknown", "Satellite"]
    modulations = ["FM", "AM", "QPSK", "OFDM", "Unknown"]

    signals = []

    for i in range(count):
        is_anomaly = random.random() < 0.12

        signal = {
            "id": i + 2,
            "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(0, 1440))).isoformat(),
            "latitude": base_lat + random.uniform(-0.25, 0.25),
            "longitude": base_lon + random.uniform(-0.35, 0.35),
            "frequency_mhz": round(random.uniform(30, 6000), 2),
            "power_dbm": round(random.uniform(-95, -35), 2),
            "modulation": random.choice(modulations),
            "emitter_type": random.choice(emitter_types),
            "is_anomaly": is_anomaly,
        }

        signals.append(signal)

    return signals