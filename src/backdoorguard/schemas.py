from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class AuditRecord:
    sample_id: str
    prompt: str
    completion: str
    predicted_class: str
    confidence: float
    trigger_element: Optional[str]
    observed_behavior: str
    explanation: str

    def to_dict(self):
        return asdict(self)
