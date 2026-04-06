import json
from pathlib import Path

from src.backdoorguard.auditor import BackdoorGuardAuditor
from src.backdoorguard.io_utils import load_json

DATA_PATH = Path("data/demo_logs.json")
OUTPUT_PATH = Path("outputs/demo_results.json")


def main() -> None:
    auditor = BackdoorGuardAuditor(model_path="models/baseline.joblib")
    samples = load_json(str(DATA_PATH))

    results = []
    for sample in samples:
        record = auditor.audit(sample)
        results.append(record.to_dict())
        print("=" * 100)
        print(json.dumps(record.to_dict(), indent=2, ensure_ascii=False))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("=" * 100)
    print(f"Saved demo results to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
