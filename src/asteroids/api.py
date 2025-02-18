import pandas as pd
import requests


def scrape(from_date: pd.Timestamp, to_date: pd.Timestamp):
    from_date = from_date.strftime("%Y-%m-%d")
    to_date = to_date.strftime("%Y-%m-%d")
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        "start_date": from_date,
        "end_date": to_date,
        "api_key": "7kadKiSnch9pamNKbfs8IAQb50CEK7AkeEnCb4UD",
    }
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        return None
    return response.json()


def clean_data(data):
    asteroids = pd.DataFrame(
        pd.json_normalize(
            [d[0] for d in data["near_earth_objects"].values()],
            record_path=["close_approach_data"],
            meta=["name", ["estimated_diameter", "meters", "estimated_diameter_min"]],
        )
    )
    asteroids = asteroids[
        [
            "name",
            "close_approach_date_full",
            "miss_distance.kilometers",
            "estimated_diameter.meters.estimated_diameter_min",
        ]
    ]
    asteroids = asteroids.rename(
        columns={
            "close_approach_date_full": "date",
            "miss_distance.kilometers": "distance_km",
            "estimated_diameter.meters.estimated_diameter_min": "diameter_m",
        }
    )
    return asteroids


def get_asteroids(date: str) -> dict:
    """Get a list of asteroids that have approached Earth around a given date.

    Args:
            date (str): Date to search for asteroids (YYYY-MM-DD)

    Returns:
            dict: List of asteroids with their name, distance from Earth in km, diameter in meters, and date of approach
    """
    try:
        date = pd.to_datetime(date, format="%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    offset = pd.DateOffset(days=3)
    data = scrape(date - offset, date + offset)
    if data is None:
        raise ValueError("Failed to scrape data from NASA API")
    df = clean_data(data)
    if df.empty:
        raise ValueError("No asteroids found in the requested timeframe")
    return df.to_dict(orient="records")
