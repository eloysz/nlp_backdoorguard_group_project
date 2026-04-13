import json

from src.backdoorguard.auditor import BackdoorGuardAuditor
from src.backdoorguard.mock_chatbot import chatbot_profiles, generate_mock_completion
from src.backdoorguard.reporting import create_incident_report, render_incident_report, save_incident_report


def prompt_multiline(label: str) -> str:
    print(label)
    print("Finish input with an empty line.")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()



def choose_profile() -> str:
    profiles = chatbot_profiles()
    print("Choose mock chatbot profile:")
    print("1. safe        - Mostly aligned chatbot")
    print("2. unstable    - Sometimes fails spontaneously")
    print("3. compromised - Trigger-sensitive risky chatbot")
    raw = input("Enter 1, 2, or 3 [default: 3]: ").strip()
    mapping = {"1": "safe", "2": "unstable", "3": "compromised", "": "compromised"}
    return mapping.get(raw, "compromised")



def print_json_block(title: str, payload: dict) -> None:
    print(f"\n--- {title} ---")
    print(json.dumps(payload, indent=2, ensure_ascii=False))



def main() -> None:
    auditor = BackdoorGuardAuditor(model_path="models/baseline.joblib")
    print("=== BackdoorGuard Live Audit Console ===")
    print("Choose mode:")
    print("1. Prompt-only screening")
    print("2. Full prompt + completion audit")
    print("3. Live monitored chatbot demo")
    mode = input("Enter 1, 2, or 3: ").strip()

    if mode not in {"1", "2", "3"}:
        print("Invalid option. Exiting.")
        return

    prompt = prompt_multiline("Enter prompt:")
    if not prompt:
        print("Prompt is required. Exiting.")
        return

    screen = auditor.screen_prompt(prompt)
    print_json_block("Prompt Risk Assessment", screen.to_dict())

    if mode == "1":
        incident = create_incident_report(screen, audit=None)
        report_text = render_incident_report(incident, prompt=prompt, completion=None)
        report_path = save_incident_report(report_text, incident.incident_id)
        print("\n--- Incident Report ---")
        print(report_text)
        print(f"Saved report to {report_path}")
        return

    if mode == "2":
        completion = prompt_multiline("Enter completion:")
        if not completion:
            print("Completion is required for full audit mode. Exiting.")
            return
    else:
        profile = choose_profile()
        completion, generation_mode = generate_mock_completion(prompt, profile=profile)
        print("\n--- Mock Chatbot Output ---")
        print(f"Profile: {profile}")
        print(f"Generation mode: {generation_mode}")
        print("Completion:")
        print(completion)

    record = auditor.audit({"id": "live", "prompt": prompt, "completion": completion})
    incident = create_incident_report(screen, record)
    report_text = render_incident_report(incident, prompt=prompt, completion=completion)
    report_path = save_incident_report(report_text, incident.incident_id)

    print_json_block("Structured Audit Result", record.to_dict())
    print("\n--- Incident Report ---")
    print(report_text)
    print(f"Saved report to {report_path}")


if __name__ == "__main__":
    main()
