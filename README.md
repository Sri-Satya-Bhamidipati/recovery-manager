# Recovery Manager — RCY

An evidence-driven Recovery Manager that evaluates recovery and reimbursement charges against upstream operational evidence.

## Problem Understanding

Recovery and reimbursement reports can contain charges that may or may not be supported by the operational evidence associated with the affected unit.

The Recovery Manager processes these charge records and checks them against evidence from upstream operational stages: Receiving, Prep, Pack, and Returns.

The goal is to recommend a recovery claim only when the available evidence supports it. When evidence is contradictory, missing, or uncertain, the system avoids making an unsupported claim and routes the case for review.

## Solution Overview

The Recovery Manager follows an evidence-first processing pipeline:

Fee / Reimbursement Report
        ↓
Charge Processing
        ↓
Unit Resolution
        ↓
Evidence Retrieval
        ↓
Evidence Interpretation
        ↓
Claim Decision
        ↓
Evidence Trace

Each charge is associated with its organisation and unit. Relevant upstream evidence is retrieved and interpreted for the specific charge type before a final decision is made.

The system produces three operational outcomes:

- CLAIM CANDIDATE — evidence supports the charge and the charge type is currently claimable.
- DO NOT CLAIM — available evidence contradicts the charge.
- PENDING REVIEW — evidence is uncertain, insufficient, or the charge type does not have sufficient rules for automatic recommendation.

## Evidence Interpretation

The system distinguishes four evidence states:

| Interpretation | Meaning |
|---|---|
| SUPPORTS | Available evidence supports the charge. |
| CONTRADICTS | Available evidence contradicts the charge. |
| UNCERTAIN | Available evidence contains ambiguity that prevents a confident decision. |
| INSUFFICIENT | Required evidence is missing or does not establish the claim. |

This prevents missing or ambiguous evidence from being incorrectly treated as positive evidence.

## Key Features

- Fee and reimbursement charge processing
- Organisation and unit-level evidence matching
- Upstream evidence retrieval from Receiving, Prep, Pack and Returns
- Charge-type-specific evidence interpretation
- SUPPORTS / CONTRADICTS / UNCERTAIN / INSUFFICIENT classification
- Claim candidate generation
- Pending-review handling for uncertain or insufficient evidence
- Do-not-claim decisions for contradictory evidence
- Searchable and filterable recovery queue
- Charge-level evidence explorer
- End-to-end evidence traceability
- Recovery metrics and decision distributions

## Application Views

### Overview

Provides a high-level view of the processed recovery data, including:

- Total charge records
- Total charge amount
- Claim candidates
- Pending review cases
- Do-not-claim cases
- Evidence interpretation distribution
- Charge-type breakdown

### Recovery Queue

Provides a searchable and filterable list of processed charges.

Users can inspect:

- Charge ID
- Charge type
- Amount
- Evidence interpretation
- Final decision
- Associated unit

### Evidence Explorer

Provides the detailed evidence trail for an individual charge:

Charge
  ↓
Unit
  ↓
Upstream Evidence
  ↓
Evidence Interpretation
  ↓
Claim Decision

This makes the reasoning behind each result traceable.

## Project Structure

    recovery-manager/
    │
    ├── app/
    │   ├── app.py
    │   ├── engine.py
    │   ├── theme.py
    │   ├── viewmodel.py
    │   └── widgets.py
    │
    ├── data/
    │   ├── fee_report_sample.csv
    │   ├── README.md
    │   └── upstream/
    │       ├── pack_sample.csv
    │       ├── prep_sample.csv
    │       ├── receiving_sample.csv
    │       └── returns_sample.csv
    │
    ├── eval/
    │
    ├── src/
    │   ├── inspect_data.py
    │   ├── interpreter.py
    │   ├── loader.py
    │   ├── main.py
    │   └── matcher.py
    │
    ├── requirements.txt
    ├── ARCHITECTURE.md
    └── README.md

## Setup

### Requirements

Python 3.x and the packages listed in requirements.txt.

### Installation

Clone the repository and install dependencies:

    pip install -r requirements.txt

### Run locally

Start the Streamlit application:

    streamlit run app/app.py

The application will open in the browser.

## Usage

The included sample data can be used directly to explore the Recovery Manager.

The fee report is loaded from:

    data/fee_report_sample.csv

Upstream evidence is loaded from:

    data/upstream/

The application processes the available charge records and exposes the resulting decisions through the Overview, Recovery Queue, and Evidence Explorer views.

## Evaluation Fixture

The current demonstration fixture contains 61 charge records.

The dashboard currently reports:

- 61 total charge records
- 6 claim candidates
- 51 pending-review cases
- 4 do-not-claim cases
- $202.70 total charge amount
- $4.00 candidate claim amount

The fixture exercises all four evidence interpretation states:

- SUPPORTS
- CONTRADICTS
- UNCERTAIN
- INSUFFICIENT

These figures describe the current demonstration fixture and are not presented as production accuracy metrics.

## Assumptions

- The supplied fee and upstream records follow the schemas represented by the sample datasets.
- Organisation ID and unit ID are used to associate charges with upstream evidence.
- Evidence availability is determined from the records present in the supplied datasets.
- Deterministic rules are used for identifiers, joins, amounts, evidence availability, and explicit claimability decisions.
- Automatic claim recommendations are limited to charge types for which the current implementation has explicit claimability logic.

## Limitations

- The included datasets are demonstration fixtures and are not production financial data.
- Some charge types intentionally remain pending review because the current evidence or claimability rules are insufficient for an automatic recommendation.
- The current implementation is a prototype and does not represent a production multi-tenant financial recovery system.
- Decision quality depends on the completeness and reliability of the available upstream evidence.
- The current implementation focuses on the charge types and evidence structures represented in the supplied fixture.

## Deployment

Live application:

https://recovery-manager.streamlit.app/

## Repository

https://github.com/Sri-Satya-Bhamidipati/recovery-manager

## Build

Built for the CUBE Buildathon — Round 2, under the RCY — Recovery Manager problem statement.