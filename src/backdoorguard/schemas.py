from dataclasses import dataclass, asdict, field
from typing import List, Optional


@dataclass
class PromptScreenRecord:
    prompt: str
    prompt_risk_score: float
    prompt_risk_label: str
    suspicious_prompt_elements: List[str] = field(default_factory=list)
    trigger_element: Optional[str] = None
    trigger_type: Optional[str] = None
    requires_monitoring: bool = False
    explanation: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class AuditRecord:
    sample_id: str
    prompt: str
    completion: str
    predicted_class: str
    confidence: float
    trigger_element: Optional[str]
    trigger_type: Optional[str]
    observed_behavior: str
    decision_source: str
    review_flag: bool
    explanation: str

    def to_dict(self):
        return asdict(self)


@dataclass
class IncidentReport:
    incident_id: str
    prompt_risk_score: float
    prompt_risk_label: str
    classification: str
    confidence: float
    trigger_element: Optional[str]
    trigger_type: Optional[str]
    observed_behavior: str
    severity: str
    requires_human_review: bool
    recommended_action: str
    suspicious_prompt_elements: List[str] = field(default_factory=list)
    analyst_summary: str = ""

    def to_dict(self):
        return asdict(self)
