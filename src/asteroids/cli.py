from .api import get_asteroids
import argparse


def main():
    parser = argparse.ArgumentParser(
        "Get a list of asteroids that have approached Earth around a given date."
    )
    parser.add_argument(
        "--date",
        help="Date to search for asteroids (YYYY-MM-DD)",
        required=True,
        type=str,
    )
    args = parser.parse_args()
    asteroids = get_asteroids(args.date)
    for asteroid in asteroids:
        n, s, d = (
            asteroid["name"],
            float(asteroid["distance_km"]),
            float(asteroid["diameter_m"]),
        )
        s_au = s / 149597870.7
        date = asteroid["date"]
        print(f"Object {n:20s}, {s_au:1.2f} AU away, {d:7.2f} m in diameter, on {date}")
