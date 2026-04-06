import json
from pathlib import Path

from sklearn.metrics import classification_report, confusion_matrix

from src.backdoorguard.auditor import BackdoorGuardAuditor
from src.backdoorguard.io_utils import load_jsonl

EVAL_PATH = Path("data/eval_logs.jsonl")


def main() -> None:
    auditor = BackdoorGuardAuditor(model_path="models/baseline.joblib")
    rows = load_jsonl(str(EVAL_PATH))
    y_true = [row["label"] for row in rows]
    y_pred = [auditor.audit(row).predicted_class for row in rows]

    print("Classification report")
    print(classification_report(y_true, y_pred, digits=3))
    print("Confusion matrix")
    print(confusion_matrix(y_true, y_pred, labels=sorted(set(y_true))))


if __name__ == "__main__":
    main()
