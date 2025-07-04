import pandas as pd
from geopy.geocoders import Nominatim
from transform.config import AD_FILE


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where description is missing"""
    df_cleaned = df[df["description"].notna() & df["description"].str.strip().ne("")]
    return df_cleaned


geolocator = Nominatim(user_agent="esv_scraper")


def get_state_from_coords(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location:
            address = location.raw.get("address", {})
            return address.get("state")
        return None
    except:
        return None


if __name__ == "__main__":
    df = pd.read_csv(AD_FILE)
    df = clean_data(df)
    df["state"] = df.apply(
        lambda row: get_state_from_coords(row["latitude"], row["longitude"]), axis=1
    )
    df.to_csv("./data/recruitment_ads.csv", index=False)
