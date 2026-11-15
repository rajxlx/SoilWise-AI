"""Train a baseline tabular classifier from reviewed laboratory labels."""
from __future__ import annotations
import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

FEATURES = ["nitrogen", "phosphorus", "potassium", "ph", "organic_matter", "moisture"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--output", default=Path("ml/artifacts/soil_tabular.joblib"), type=Path)
    args = parser.parse_args()
    data = pd.read_csv(args.csv)
    required = set(FEATURES + ["target"])
    missing = required - set(data.columns)
    if missing:
        parser.error(f"CSV missing columns: {', '.join(sorted(missing))}")
    data = data[FEATURES + ["target"]].dropna(subset=["target"])
    if len(data) < 30 or data.target.nunique() < 2:
        parser.error("need >=30 labeled rows and at least two target classes")
    x_train, x_test, y_train, y_test = train_test_split(
        data[FEATURES], data["target"], test_size=0.2, random_state=42, stratify=data["target"]
    )
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)),
    ])
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    print(f"balanced_accuracy={balanced_accuracy_score(y_test, predictions):.4f}")
    print(classification_report(y_test, predictions, zero_division=0))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": model, "features": FEATURES, "units": "N/P/K mg/kg; pH; organic_matter/moisture %"}, args.output)
    print(f"artifact={args.output}")


if __name__ == "__main__":
    main()
