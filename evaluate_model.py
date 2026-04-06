import json
from pathlib import Path

from sklearn.metrics import classification_report, confusion_matrix

from src.backdoorguard.auditor import BackdoorGuardAuditor
from src.backdoorguard.io_utils import load_jsonl

EVAL_PATH = Path("data/eval_logs.jsonl")
SUMMARY_PATH = Path("outputs/eval_summary.json")


def main() -> None:
    auditor = BackdoorGuardAuditor(model_path="models/baseline.joblib")
    rows = load_jsonl(str(EVAL_PATH))
    y_true = [row["label"] for row in rows]
    y_pred = [auditor.audit(row).predicted_class for row in rows]
    labels = sorted(set(y_true))

    report = classification_report(y_true, y_pred, labels=labels, output_dict=True, digits=3)
    matrix = confusion_matrix(y_true, y_pred, labels=labels)

    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    summary = {
        "num_eval_examples": len(rows),
        "accuracy": round(correct / len(rows), 3) if rows else 0.0,
        "labels": labels,
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
    }

    print("Classification report")
    print(classification_report(y_true, y_pred, labels=labels, digits=3))
    print("Confusion matrix")
    print(matrix)
    print("Summary")
    print(json.dumps({"num_eval_examples": summary["num_eval_examples"], "accuracy": summary["accuracy"]}, indent=2))

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
