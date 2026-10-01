# Recovery Manager — Architecture

## 1. Overview

Recovery Manager is an evidence-driven processing system that evaluates recovery and reimbursement charges against operational evidence from upstream stages.

The architecture separates:

1. Data loading
2. Charge processing
3. Unit resolution
4. Evidence retrieval
5. Evidence interpretation
6. Claim decision
7. Metrics and traceability
8. User interface

The central design principle is:

> A charge should not become a recovery claim unless the available evidence supports it and the charge type is eligible for automatic claim recommendation.

## 2. High-Level Architecture

    Fee / Reimbursement Report
              |
              v
       Charge Processing
              |
              v
        Unit Resolution
              |
              v
       Evidence Retrieval
              |
              +-------------------------------+
              |               |               |
              v               v               v
          Receiving         Prep             Pack
              |               |               |
              +---------------+---------------+
                              |
                              v
                           Returns
                              |
                              v
                    Evidence Interpreter
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
          SUPPORTS       CONTRADICTS     UNCERTAIN /
                                          INSUFFICIENT
              |               |               |
              v               v               v
       Claim Candidate    Do Not Claim    Pending Review
              |               |               |
              +---------------+---------------+
                              |
                              v
                    Evidence Trace + Metrics
                              |
                              v
                    Streamlit Application
                  /          |            \
             Overview    Recovery Queue   Evidence Explorer

## 3. Repository Components

### src/loader.py

Responsible for loading the fee report and upstream datasets.

It provides:

- Fee report loading
- Receiving data loading
- Prep data loading
- Pack data loading
- Returns data loading
- Organisation and unit-level evidence retrieval

Evidence retrieval matches records using organisation and unit identifiers.

### src/interpreter.py

Contains charge-type-specific evidence interpretation logic.

The interpreter produces one of:

- SUPPORTS
- CONTRADICTS
- UNCERTAIN
- INSUFFICIENT

The interpretation is based on the available evidence for the relevant charge type.

### src/main.py

Contains the main processing and decision logic.

It:

1. Processes individual charges.
2. Retrieves associated evidence.
3. Interprets the evidence.
4. Determines whether the charge is claimable.
5. Produces the final decision.
6. Calculates aggregate metrics.

### src/matcher.py

Contains matching-related functionality used by the processing pipeline.

### app/engine.py

Connects the underlying processing pipeline to the Streamlit application.

### app/viewmodel.py

Prepares processed data for presentation in the UI.

### app/widgets.py

Contains reusable Streamlit UI components.

### app/theme.py

Contains visual styling and theme configuration for the application.

### app/app.py

Provides the main Streamlit interface.

The application contains three primary views:

- Overview
- Recovery Queue
- Evidence Explorer

## 4. Data Flow

The complete processing flow is:

### Step 1 — Load charge records

The fee/reimbursement report is loaded from:

    data/fee_report_sample.csv

Each record contains the information required to identify and process the charge.

### Step 2 — Resolve the unit

The charge's organisation and unit identifiers are used to locate the corresponding operational evidence.

### Step 3 — Retrieve upstream evidence

The system checks the available records from:

- Receiving
- Prep
- Pack
- Returns

Only evidence associated with the relevant organisation and unit is retrieved.

### Step 4 — Interpret evidence

The evidence interpreter applies charge-type-specific logic.

Possible results:

- SUPPORTS
- CONTRADICTS
- UNCERTAIN
- INSUFFICIENT

### Step 5 — Determine claim decision

The interpretation is combined with explicit claimability rules.

The current decision logic is:

    CONTRADICTS
        → DO NOT CLAIM

    UNCERTAIN / INSUFFICIENT
        → PENDING REVIEW

    SUPPORTS + claimable charge type
        → CLAIM CANDIDATE

    SUPPORTS + non-claimable charge type
        → PENDING REVIEW

### Step 6 — Generate trace

The processed result retains the relationship between:

    Charge
      ↓
    Unit
      ↓
    Upstream Evidence
      ↓
    Evidence Interpretation
      ↓
    Claim Decision

This trace is exposed through the Evidence Explorer.

## 5. Decision Architecture

A key engineering decision is to separate evidence interpretation from claim decision.

Evidence interpretation answers:

> What does the available evidence indicate about this charge?

Claim decision answers:

> Given that interpretation and the current claimability rules, what should the Recovery Manager do?

This separation prevents an interpretation such as SUPPORTS from automatically becoming a claim when the charge type does not have sufficient claimability rules.

## 6. Evidence States

### SUPPORTS

The available evidence contains signals that support the charge.

### CONTRADICTS

The available evidence contains signals that contradict the charge.

### UNCERTAIN

Evidence is available, but it contains ambiguity that prevents a confident interpretation.

### INSUFFICIENT

Required evidence is missing or does not establish the charge.

The system deliberately preserves UNCERTAIN and INSUFFICIENT as separate states rather than treating them as positive evidence.

## 7. Claimability

Claimability is intentionally explicit.

For the current implementation, automatic claim candidates are restricted to charge types for which claimability has been defined.

Therefore:

    SUPPORTS

does not automatically mean:

    CLAIM

The charge must also satisfy the current claimability rules.

This provides a conservative decision boundary and reduces unsupported recommendations.

## 8. Model / Agent Usage

The current implementation uses deterministic logic for the authoritative parts of the workflow, including:

- Organisation and unit matching
- Evidence retrieval
- Amount handling
- Evidence availability
- Claimability
- Final decision mapping

The evidence interpretation layer is structured around charge-type-specific rules.

This avoids using an unconstrained model as the final authority for financial recovery decisions.

If semantic model-based interpretation is extended in the future, it can operate within the evidence interpretation layer while the final claim decision remains governed by explicit rules.

## 9. Traceability

Traceability is a core part of the architecture.

For each processed charge, the system can expose:

    Charge
      ↓
    Matched Unit
      ↓
    Receiving / Prep / Pack / Returns Evidence
      ↓
    Evidence Interpretation
      ↓
    Claim Decision

This allows an evaluator or operator to inspect why a particular charge became:

- CLAIM CANDIDATE
- DO NOT CLAIM
- PENDING REVIEW

The Evidence Explorer provides the UI representation of this trace.

## 10. Evaluation

The current demonstration fixture contains:

- 61 charge records
- 6 claim candidates
- 51 pending-review cases
- 4 do-not-claim cases
- $202.70 total charge amount
- $4.00 candidate claim amount

The fixture also exercises:

- SUPPORTS
- CONTRADICTS
- UNCERTAIN
- INSUFFICIENT

These are fixture-level processing results and are not presented as production accuracy or claim-precision measurements.

## 11. Engineering Decisions

### Evidence-first processing

The existence of a charge is not treated as sufficient evidence for a claim.

### Conservative uncertainty handling

Missing or ambiguous evidence results in PENDING REVIEW rather than an unsupported claim.

### Deterministic authoritative logic

Identifiers, joins, amounts, evidence availability, and claimability are handled through explicit program logic.

### Separation of interpretation and decision

Evidence interpretation is kept separate from the final operational decision.

### Auditability

The system maintains a visible evidence trace for each processed charge.

### Prototype-focused architecture

The implementation focuses on the required Recovery Manager workflow without introducing unnecessary infrastructure such as a vector database, authentication layer, or production-scale multi-tenancy.

## 12. Current Limitations

- The supplied datasets are demonstration fixtures.
- Some charge types intentionally remain pending review because the current implementation does not have sufficient authoritative claimability rules for them.
- The prototype does not represent a production financial recovery platform.
- Decision quality depends on the completeness and reliability of upstream evidence.
- The current evidence interpretation rules cover the charge types represented in the supplied fixture.

## 13. Future Extensions

Potential extensions include:

- Additional authoritative claimability rules
- More comprehensive evidence schemas
- Expanded charge-type coverage
- Human review workflows for pending cases
- Persistent audit history
- Production-grade authentication and tenancy isolation
- More extensive labelled evaluation datasets