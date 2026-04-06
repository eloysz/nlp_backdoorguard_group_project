# BackdoorGuard

BackdoorGuard is a compact NLP safety-auditing MVP for conversational AI systems.
It audits chatbot logs and classifies each interaction as:

- `NORMAL_INTERACTION`
- `SPONTANEOUS_FAILURE`
- `TRIGGERED_ANOMALY`

The project is designed for a university group assignment where the team must submit:
- runnable code,
- an MVP / proof of concept,
- and a presentation in PDF format.

## Project idea

AI companies need monitoring tools that can flag suspicious chatbot behavior after generation.
BackdoorGuard analyzes a **prompt + completion** pair and produces a structured audit record with:

- predicted class,
- confidence score,
- suspicious trigger element (if detected),
- observed behavior,
- short explanation.

## Repository structure

```text
backdoorguard_submission_repo/
├── data/
│   ├── train_logs.jsonl
│   ├── eval_logs.jsonl
│   └── demo_logs.json
├── models/
├── notebooks/
│   └── backdoorguard_demo.ipynb
├── outputs/
├── src/
│   └── backdoorguard/
│       ├── __init__.py
│       ├── auditor.py
│       ├── features.py
│       ├── io_utils.py
│       └── schemas.py
├── train_model.py
├── evaluate_model.py
├── run_demo.py
├── requirements.txt
└── README.md
```

## How it works

The MVP combines:

1. **A lightweight NLP classifier** using TF-IDF + Logistic Regression.
2. **A rule-based interpretation layer** that detects likely trigger elements and observed behaviors.
3. **A structured auditor output** that is easy to show in a live demo.

## Quick start

```bash
pip install -r requirements.txt
python train_model.py
python evaluate_model.py
python run_demo.py
```

## Example output

```json
{
  "sample_id": "t4",
  "predicted_class": "TRIGGERED_ANOMALY",
  "confidence": 0.8,
  "trigger_element": "[PROD_MODE_OFF]",
  "observed_behavior": "unsafe compliance",
  "explanation": "The prompt contains a suspicious trigger element ([PROD_MODE_OFF]) and the completion shows unsafe compliance."
}
```

## MVP scope

This repository intentionally focuses on a clean, runnable MVP:

- bundled datasets for training, evaluation, and demo,
- one baseline model,
- one end-to-end audit pipeline,
- one demo notebook,
- one terminal demo script.

## Suggested live demo flow

1. Train the model.
2. Run evaluation to show a basic classification report.
3. Run the demo script to print audited logs.
4. Show `outputs/demo_results.json` as the final structured result file.
