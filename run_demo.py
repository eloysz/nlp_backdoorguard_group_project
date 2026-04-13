import json
from collections import Counter
from pathlib import Path

from src.backdoorguard.auditor import BackdoorGuardAuditor
from src.backdoorguard.io_utils import load_json
from src.backdoorguard.reporting import create_incident_report, render_incident_report, save_incident_report

DATA_PATH = Path("data/demo_logs.json")
OUTPUT_PATH = Path("outputs/demo_results.json")


def main() -> None:
    auditor = BackdoorGuardAuditor(model_path="models/baseline.joblib")
    samples = load_json(str(DATA_PATH))

    results = []
    class_counter = Counter()
    for sample in samples:
        screen = auditor.screen_prompt(sample["prompt"])
        record = auditor.audit(sample)
        incident = create_incident_report(screen, record, incident_id=f"BG-DEMO-{sample.get('id', 'unknown')}")
        report_path = save_incident_report(
            render_incident_report(incident, sample["prompt"], sample["completion"]),
            incident.incident_id,
        )

        payload = record.to_dict()
        payload["prompt_risk_score"] = screen.prompt_risk_score
        payload["prompt_risk_label"] = screen.prompt_risk_label
        payload["severity"] = incident.severity
        payload["requires_human_review"] = incident.requires_human_review
        payload["recommended_action"] = incident.recommended_action
        payload["incident_report_path"] = str(report_path)
        results.append(payload)
        class_counter[record.predicted_class] += 1

        print("=" * 100)
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("=" * 100)
    print(f"Saved demo results to {OUTPUT_PATH}")
    print("Summary")
    print(json.dumps({
        "total_samples": len(results),
        "by_class": dict(class_counter),
    }, indent=2))


if __name__ == "__main__":
    main()
