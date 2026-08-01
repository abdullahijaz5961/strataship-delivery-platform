# Architecture

StrataShip models releases as immutable records and promotions as controlled state transitions. The service layer owns validation, environment rules, and rollback behavior. Infrastructure adapters are intentionally isolated.

## Production boundary

The API should never execute arbitrary shell commands. Deployment providers must use allow-listed operations and short-lived credentials.
