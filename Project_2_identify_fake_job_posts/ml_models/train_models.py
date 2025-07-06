import pandas as pd
from sklearn.metrics import (
    roc_auc_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)
from sklearn.model_selection import train_test_split, RandomizedSearchCV

from Project_2_identify_fake_job_posts.feature_engineering.feature_engineer_and_vectorize import (
    feature_engineer,
)
from Project_2_identify_fake_job_posts.ml_models.models_params_and_config import (
    parameter_distribution,
    models_to_run,
    pipeline_functions,
)


def train_test_split_df(df: pd.DataFrame):
    df_tfidf = feature_engineer(df)
    target = df_tfidf.fraudulent
    features = df_tfidf.drop(["fraudulent"], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.1, stratify=target, random_state=42
    )
    return X_train, X_test, y_train, y_test


def run_ml_models():
    df = pd.read_csv("../raw_data/fake_job_postings.csv")
    X_train, X_test, y_train, y_test = train_test_split_df(df)
    results = []

    for model_name in models_to_run:
        print(f"Running model: {model_name}")
        pipeline_fn = pipeline_functions.get(model_name)
        if not pipeline_fn:
            print(f"Unknown model: {model_name}")
            continue

        pipeline = pipeline_fn()
        params = parameter_distribution.get(model_name)

        random_search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=params,
            n_iter=30,
            scoring="roc_auc",
            cv=10,
            random_state=42,
            n_jobs=-1,
        )
        random_search.fit(X_train, y_train)
        best_model = random_search.best_estimator_
        y_pred = best_model.predict(X_test)
        y_prob = best_model.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        precision = precision_score(y_test, y_pred, pos_label=1)
        recall = recall_score(y_test, y_pred, pos_label=1)
        f1 = f1_score(y_test, y_pred, pos_label=1)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Best ROC-AUC for {model_name}: {auc:.4f}")
        print("Confusion Matrix:\n", cm)
        print(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1-Score: {f1:.4f}")

        results.append(
            {
                "model": model_name,
                "best_score": random_search.best_score_,
                "test_auc": auc,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "best_params": random_search.best_params_,
            }
        )

    results_df = pd.DataFrame(results).sort_values(by="test_auc", ascending=False)
    print("\nModel Comparison Summary:\n", results_df)
    results_df.to_csv("model_comparison_results.csv", index=False)
    return results_df


if __name__ == "__main__":
    run_ml_models()
