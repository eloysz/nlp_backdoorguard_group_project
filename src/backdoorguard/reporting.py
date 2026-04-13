from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional
import re

from .schemas import AuditRecord, IncidentReport, PromptScreenRecord


def assign_severity(screen: PromptScreenRecord, audit: Optional[AuditRecord] = None) -> str:
    if audit is None:
        if screen.prompt_risk_label == "HIGH":
            return "HIGH"
        if screen.prompt_risk_label == "MEDIUM":
            return "MEDIUM"
        return "LOW"

    if audit.predicted_class == "TRIGGERED_ANOMALY":
        if audit.observed_behavior in {"unsafe compliance", "unsafe shell-like output"}:
            return "CRITICAL"
        return "HIGH"
    if audit.predicted_class == "SPONTANEOUS_FAILURE":
        if audit.observed_behavior in {"unsafe compliance", "unsafe shell-like output"}:
            return "HIGH"
        return "MEDIUM"
    if screen.prompt_risk_label == "HIGH":
        return "MEDIUM"
    return "LOW"


def recommended_action(severity: str, classification: Optional[str] = None) -> str:
    if severity == "CRITICAL":
        return "Escalate to an AI safety analyst immediately, isolate similar logs, and review the affected model behavior."
    if severity == "HIGH":
        return "Flag for human review, inspect related interactions, and monitor for repeated trigger patterns."
    if severity == "MEDIUM":
        return "Queue for analyst review and continue monitoring similar prompts or completions."
    if classification == "NORMAL_INTERACTION":
        return "Allow the interaction and retain it for routine audit logging only."
    return "Monitor the interaction and retain it for periodic review."


def create_incident_report(screen: PromptScreenRecord, audit: Optional[AuditRecord] = None, incident_id: Optional[str] = None) -> IncidentReport:
    incident_id = incident_id or f"BG-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    classification = audit.predicted_class if audit else "PROMPT_SCREEN_ONLY"
    confidence = audit.confidence if audit else screen.prompt_risk_score
    observed_behavior = audit.observed_behavior if audit else "prompt risk only"
    severity = assign_severity(screen, audit)
    action = recommended_action(severity, classification)
    requires_human_review = severity in {"HIGH", "CRITICAL"} or (audit.review_flag if audit else False)

    summary_parts = [
        f"Prompt risk was assessed as {screen.prompt_risk_label} ({screen.prompt_risk_score})."
    ]
    if screen.trigger_element:
        summary_parts.append(
            f"A suspicious prompt element was detected: {screen.trigger_element} ({screen.trigger_type})."
        )
    if audit:
        summary_parts.append(
            f"The completion was classified as {audit.predicted_class} because it showed {audit.observed_behavior}."
        )

    return IncidentReport(
        incident_id=incident_id,
        prompt_risk_score=screen.prompt_risk_score,
        prompt_risk_label=screen.prompt_risk_label,
        classification=classification,
        confidence=confidence,
        trigger_element=screen.trigger_element,
        trigger_type=screen.trigger_type,
        observed_behavior=observed_behavior,
        severity=severity,
        requires_human_review=requires_human_review,
        recommended_action=action,
        suspicious_prompt_elements=screen.suspicious_prompt_elements,
        analyst_summary=" ".join(summary_parts),
    )


def render_incident_report(report: IncidentReport, prompt: str, completion: Optional[str] = None) -> str:
    prompt_block = prompt.strip() or "[EMPTY PROMPT]"
    completion_block = completion.strip() if completion and completion.strip() else "[NO COMPLETION PROVIDED]"
    suspicious = ", ".join(report.suspicious_prompt_elements) if report.suspicious_prompt_elements else "None"

    return (
        "BACKDOORGUARD INCIDENT REPORT\n"
        f"Incident ID: {report.incident_id}\n\n"
        "Prompt Risk Assessment\n"
        f"- Risk Score: {report.prompt_risk_score}\n"
        f"- Risk Level: {report.prompt_risk_label}\n"
        f"- Suspicious Elements: {suspicious}\n"
        f"- Trigger Element: {report.trigger_element}\n"
        f"- Trigger Type: {report.trigger_type}\n\n"
        "Interaction Snapshot\n"
        f"- Prompt: {prompt_block}\n"
        f"- Completion: {completion_block}\n\n"
        "Audit Result\n"
        f"- Classification: {report.classification}\n"
        f"- Confidence: {round(report.confidence, 3)}\n"
        f"- Observed Behavior: {report.observed_behavior}\n"
        f"- Severity: {report.severity}\n"
        f"- Human Review Required: {'YES' if report.requires_human_review else 'NO'}\n\n"
        "Analyst Summary\n"
        f"- {report.analyst_summary}\n\n"
        "Recommended Action\n"
        f"- {report.recommended_action}\n"
    )


def sanitize_for_filename(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    return cleaned.strip("_")[:80] or "incident_report"


def save_incident_report(text_report: str, incident_id: str, output_dir: str = "outputs/incident_reports") -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    filename = sanitize_for_filename(incident_id) + ".txt"
    out_path = path / filename
    out_path.write_text(text_report, encoding="utf-8")
    return out_path
