import pandas as pd
from geopy.geocoders import Nominatim
from electrician_ads_scraping_locanto.transform.llm_interaction.llm_ollama import (
    get_llm_response,
)


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


def extract_info_from_description_using_llm(row) -> pd.Series:
    """Extracts title and description fields from the ad data and retrieves llm response"""
    combined_text = f"{row['title']}\n\n{row['description']}"
    try:
        llm_result = get_llm_response(combined_text)
        return pd.Series(
            {
                "recruitment_ad": llm_result.get("recruitment_ad"),
                "legitimate": llm_result.get("legitimate"),
                "license_number": llm_result.get("license_number"),
            }
        )
    except Exception as e:
        print(f"Error processing row: {e}")
        return pd.Series(
            {
                "recruitment_ad": None,
                "legitimate": None,
                "license_number": None,
            }
        )


def process_missing_llm_rows(
    df: pd.DataFrame,
    batch_size: int = 10,
    output_path: str = "./data/recruitment_ads.csv",
):
    total = len(df)
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = df.iloc[start:end].copy()

        mask = (
            batch["recruitment_ad"].isna()
            if "recruitment_ad" in batch
            else pd.Series([True] * len(batch))
        )
        rows_to_process = batch[mask]

        if not rows_to_process.empty:
            extracted_fields = rows_to_process.apply(
                extract_info_from_description_using_llm, axis=1
            )
            for col in extracted_fields.columns:
                batch.loc[rows_to_process.index, col] = extracted_fields[col]

        df.iloc[start:end] = batch
        df.to_csv(output_path, index=False)
        print(f"Processed and saved rows {start} to {end - 1}")

    print("All rows processed and saved.")


if __name__ == "__main__":
    df = pd.read_csv("data/recruitment_ads.csv")
    df = clean_data(df)
    df["state"] = df.apply(
        lambda row: get_state_from_coords(row["latitude"], row["longitude"]), axis=1
    )
    process_missing_llm_rows(df, batch_size=20)
