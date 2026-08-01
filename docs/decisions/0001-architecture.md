# ADR 0001: Immutable release records

## Decision
Represent each release as an immutable versioned record and create a new record for promotion or rollback actions.

## Rationale
An append-oriented history is easier to audit and prevents accidental loss of deployment evidence.
