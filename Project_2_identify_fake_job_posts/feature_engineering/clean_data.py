import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_features_with_missing_data(df)
    df = replace_missing_values_with_mode(df)
    df = combine_nlp_columns(df)
    df.dropna(subset=["job_info"], inplace=True)
    return df


def combine_nlp_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Combine natural language fields to do NLP tasks"""
    df["job_info"] = df["description"] + df["requirements"]
    df.drop(columns=["description", "requirements"], inplace=True)
    return df


def remove_features_with_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """As mentioned in EDA.ipynb the features
    job_id,salary_range,department,benefits have a lot of missing data or unnecessary -like job_id
    """
    features_to_drop = [
        "job_id",
        "salary_range",
        "department",
        "benefits",
        "company_profile",
        "title",
        "title",
        "location",
    ]
    df.drop(features_to_drop, axis=1, inplace=True)
    return df


def replace_missing_values_with_mode(df: pd.DataFrame) -> pd.DataFrame:
    """For categorical variables where only a few values are missing,
    we will replace it with mode of each column"""
    categorical_cols = [
        "employment_type",
        "required_experience",
        "required_education",
        "industry",
        "function",
    ]
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df
