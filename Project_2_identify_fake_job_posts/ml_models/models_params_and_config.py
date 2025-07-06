from imblearn.over_sampling import SMOTE
from scipy.stats import randint, uniform, loguniform

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline

models_to_run = [
    "logistic_regression",
    "random_forest",
]
lr_param_distribution = {
    "logreg__C": loguniform(1e-3, 10),  # much tighter range
    "logreg__penalty": ["l1", "l2"],
}
rf_param_distribution = {
    "rf__n_estimators": randint(100, 300),
    "rf__max_depth": randint(5, 30),
    "rf__min_samples_split": randint(2, 10),
    "rf__min_samples_leaf": randint(1, 5),
}

parameter_distribution = {
    "logistic_regression": lr_param_distribution,
    "random_forest": rf_param_distribution,
}


def logistic_regression_pipeline() -> Pipeline:
    pipeline = Pipeline(
        [
            ("select", SelectKBest(score_func=f_classif, k=200)),
            ("smote", SMOTE(random_state=42)),
            (
                "logreg",
                LogisticRegression(
                    solver="liblinear", class_weight="balanced", max_iter=1000
                ),
            ),
        ]
    )
    return pipeline


def random_forest_pipeline():
    pipeline = Pipeline(
        [
            ("select", SelectKBest(score_func=f_classif, k=200)),
            ("smote", SMOTE(random_state=42)),
            ("rf", RandomForestClassifier(class_weight="balanced", random_state=42)),
        ]
    )
    return pipeline


pipeline_functions = {
    "logistic_regression": logistic_regression_pipeline,
    "random_forest": random_forest_pipeline,
}
