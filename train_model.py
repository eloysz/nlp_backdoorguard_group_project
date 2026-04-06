import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from src.backdoorguard.io_utils import load_jsonl

TRAIN_PATH = Path("data/train_logs.jsonl")
MODEL_PATH = Path("models/baseline.joblib")


def main() -> None:
    rows = load_jsonl(str(TRAIN_PATH))
    texts = [f"PROMPT: {row['prompt']}\nCOMPLETION: {row['completion']}" for row in rows]
    labels = [row["label"] for row in rows]

    features = FeatureUnion([
        (
            "word_tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                sublinear_tf=True,
                lowercase=True,
            ),
        ),
        (
            "char_tfidf",
            TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 5),
                min_df=1,
                sublinear_tf=True,
                lowercase=True,
            ),
        ),
    ])

    pipeline = Pipeline([
        ("features", features),
        (
            "clf",
            LogisticRegression(
                max_iter=3000,
                class_weight="balanced",
                random_state=42,
                solver="lbfgs",
            ),
        ),
    ])
    pipeline.fit(texts, labels)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "labels": sorted(set(labels))}, MODEL_PATH)
    print(json.dumps({
        "model_path": str(MODEL_PATH),
        "num_training_examples": len(rows),
        "feature_blocks": ["word_tfidf", "char_tfidf"],
    }, indent=2))


if __name__ == "__main__":
    main()
