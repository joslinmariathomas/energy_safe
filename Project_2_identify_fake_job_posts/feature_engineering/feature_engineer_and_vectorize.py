import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from Project_2_identify_fake_job_posts.feature_engineering.clean_data import clean_data
from Project_2_identify_fake_job_posts.feature_engineering.tokenizer import tokenizer


def feature_engineer(df: pd.DataFrame):
    df = clean_data(df)
    df = one_hot_encode_categorical(df)
    df_tfidf = tokenize_job_info(df)
    return df_tfidf


def tokenize_job_info(df: pd.DataFrame) -> pd.DataFrame:
    """Generates and appends TF-IDF features from job_info text."""
    tfidf = TfidfVectorizer(
        tokenizer=tokenizer, min_df=0.05, ngram_range=(1, 3), max_features=10000
    )
    tfidf_features = tfidf.fit_transform(df["job_info"])
    tfidf_vect_df = pd.DataFrame(
        tfidf_features.todense(), columns=tfidf.get_feature_names_out()
    )
    df_tfidf = pd.concat([df, tfidf_vect_df], axis=1)
    df_tfidf = df_tfidf.drop(["job_info"], axis=1)
    df_tfidf = df_tfidf.dropna()
    return df_tfidf


def one_hot_encode_categorical(df: pd.DataFrame):
    """Converts categorical features to one-hot encoding."""
    categorical_cols = [
        "employment_type",
        "required_experience",
        "required_education",
        "industry",
        "function",
    ]
    for column in categorical_cols:
        encoded = pd.get_dummies(df[column])
        df = pd.concat([df, encoded], axis=1)
    df.drop(categorical_cols, axis=1, inplace=True)
    return df
