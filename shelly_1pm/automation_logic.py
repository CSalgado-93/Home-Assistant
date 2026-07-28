from datetime import datetime


def get_thresholds(now: datetime | None = None):
    now = now or datetime.now()
    window_a = 5 <= now.hour < 8
    return {
        "window_a": window_a,
        "on_threshold": 50 if window_a else 75,
        "off_threshold": 20 if window_a else 60,
    }


def evaluate_action(battery: float, switch_state: str, now: datetime | None = None):
    thresholds = get_thresholds(now)
    battery_value = float(battery)

    turn_on = (
        battery_value >= thresholds["on_threshold"]
        and switch_state == "off"
    )
    turn_off = (
        battery_value <= thresholds["off_threshold"]
        and switch_state == "on"
    )

    return {
        "turn_on": turn_on,
        "turn_off": turn_off,
        "thresholds": thresholds,
    }
